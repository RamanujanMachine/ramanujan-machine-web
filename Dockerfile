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

COPY ./react-frontend ./ 

# install node package dependencies
RUN npm install

# Build frontend project
RUN npm run build

# copy API files
COPY ./python-backend/Pipfile* ./
COPY ./python-backend/*.py ./
COPY ./python-backend/requirements.txt ./

# install Python dependencies
RUN python3 -m venv venv
RUN chmod +x venv/bin/activate
RUN ./venv/bin/activate
RUN pip3 install -r requirements.txt --break-system-packages
RUN pip3 install uvicorn --break-system-packages

EXPOSE 80
EXPOSE 8000

COPY docker_start.sh docker_start.sh
RUN chmod +x docker_start.sh
CMD ./docker_start.sh
