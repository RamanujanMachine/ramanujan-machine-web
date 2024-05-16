# syntax=docker/dockerfile:1
# This docker container runs the web portal
FROM ubuntu:latest
LABEL description="Ramanujan Machine Web Portal"

# set working directory
WORKDIR /srv/ramanujan-machine-web-portal

# set env var for Wolfram API token which should be passed in via docker build
ARG wolfram_app_id
ENV WOLFRAM_APP_ID=$wolfram_app_id

# install system dependencies
RUN apt-get update
RUN apt-get -y install ca-certificates
RUN apt-get -y install python3 python3-pip python3-venv 
RUN apt-get -y install curl gnupg 
RUN apt-get -y install libpq-dev libgmp-dev libgmp3-dev libmpfr-dev libmpc-dev
RUN apt-get install -y npm
RUN npm i -g n && n lts && npm i -g npm@latest

# install NodeJS
#RUN mkdir -p /etc/apt/keyrings
#RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
#ENV NODE_MAJOR=22
#RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
#RUN apt-get update && apt-get -y install nodejs

# React frontend
COPY react-frontend ./react-frontend
WORKDIR /srv/ramanujan-machine-web-portal/react-frontend
# install NodeJS dependencies
RUN npm install
# generate deployable artifacts
RUN npm run build

# create virtual environment for FastAPI web server and install dependencies
WORKDIR /srv/ramanujan-machine-web-portal
ENV BKPATH=$PATH
COPY python-backend ./python-backend
RUN cp -rf react-frontend/build python-backend/build
WORKDIR /srv/ramanujan-machine-web-portal/python-backend
RUN rm -rf venv
RUN python3 -m venv venv
#RUN chmod +x venv/bin/activate
RUN . venv/bin/activate
RUN ./venv/bin/python -m pip install uvicorn
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
#RUN chmod +x venv/bin/activate
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
EXPOSE 8000

# start web and gRPC servers
WORKDIR /srv/ramanujan-machine-web-portal
COPY docker_start.sh ./docker_start.sh
RUN chmod +x docker_start.sh
CMD ./docker_start.sh
