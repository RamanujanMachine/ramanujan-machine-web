# syntax=docker/dockerfile:1
# This docker container runs the web portal
FROM ubuntu:latest
LABEL description="Ramanujan Machine Web Portal"

# set working directory
WORKDIR /srv/ramanujan-machine-web-portal

# install node
RUN apt-get update && apt-get -y install git python3 python3-pip python3.10-venv ca-certificates curl gnupg libpq-dev libgmp-dev libmpfr-dev libmpc-dev

RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
ENV NODE_MAJOR=20
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list

RUN apt-get update && apt-get -y install nodejs

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
RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn

EXPOSE 5173
EXPOSE 8000

COPY docker_start.sh docker_start.sh
RUN chmod +x docker_start.sh
CMD ./docker_start.sh
