# syntax=docker/dockerfile:1
# This docker container runs the web portal
FROM ubuntu:latest
LABEL description="Ramanujan Machine Web Portal"

# set working directory
WORKDIR /srv/ramanujan-machine-web-portal

ARG public_ip
ENV PUBLIC_IP=$public_ip

# install system dependencies
RUN apt-get update
RUN apt-get -y install ca-certificates
RUN apt-get -y install python3 python3-pip python3-venv 
RUN apt-get -y install curl gnupg 
RUN apt-get -y install libpq-dev libgmp-dev libgmp3-dev libmpfr-dev libmpc-dev
RUN apt-get install -y npm
RUN npm i -g n && n lts && npm i -g npm@latest

# React frontend
COPY react-frontend ./react-frontend
WORKDIR /srv/ramanujan-machine-web-portal/react-frontend
# install NodeJS dependencies
RUN npm ci
RUN echo "VITE_PUBLIC_IP=${PUBLIC_IP}" > .env.production
# generate deployable artifacts
RUN npm run build

# create virtual environment for FastAPI web server and install dependencies
WORKDIR /srv/ramanujan-machine-web-portal
ENV BKPATH=$PATH
COPY python-backend ./python-backend
RUN cp -rf react-frontend/build python-backend/build
WORKDIR /srv/ramanujan-machine-web-portal/python-backend
RUN --mount=type=secret,id=creds cat /run/secrets/creds >> .env
RUN rm -rf venv
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN ./venv/bin/python -m pip install -r /srv/ramanujan-machine-web-portal/python-backend/requirements.txt
ENV PATH=$BKPATH
RUN unset VIRTUAL_ENV

# create virtual environment for gRPC server and install dependencies
WORKDIR /srv/ramanujan-machine-web-portal
COPY protos ./protos
COPY lirec-grpc-server ./lirec-grpc-server
WORKDIR /srv/ramanujan-machine-web-portal/lirec-grpc-server
RUN rm -rf venv
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN venv/bin/python -m pip install -r requirements.txt
ENV PATH=$BKPATH
RUN unset VIRTUAL_ENV

# generate gRPC code in both client (web server) and gRPC server directories
WORKDIR /srv/ramanujan-machine-web-portal
RUN pip install grpcio grpcio-tools --break-system-packages
WORKDIR /srv/ramanujan-machine-web-portal/python-backend
RUN python3 -m grpc_tools.protoc --proto_path=/srv/ramanujan-machine-web-portal/protos --python_out=/srv/ramanujan-machine-web-portal/python-backend/ --grpc_python_out=/srv/ramanujan-machine-web-portal/python-backend/ /srv/ramanujan-machine-web-portal/protos/lirec.proto
WORKDIR /srv/ramanujan-machine-web-portal/lirec-grpc-server
RUN python3 -m grpc_tools.protoc --proto_path=/srv/ramanujan-machine-web-portal/protos --python_out=/srv/ramanujan-machine-web-portal/lirec-grpc-server/ --grpc_python_out=/srv/ramanujan-machine-web-portal/lirec-grpc-server/ /srv/ramanujan-machine-web-portal/protos/lirec.proto

# expose web port
EXPOSE 80

# start web and gRPC servers
WORKDIR /srv/ramanujan-machine-web-portal
COPY docker_start.sh ./docker_start.sh
RUN chmod +x docker_start.sh
CMD ./docker_start.sh
