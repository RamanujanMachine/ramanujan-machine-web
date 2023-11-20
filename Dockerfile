# syntax=docker/dockerfile:1
# This docker container runs the web portal
# Slim Linux image
FROM alpine:latest
LABEL description="Ramanujan Machine Web Portal"

# set working directory
WORKDIR /srv/ramanujan-machine-portal

# install node
RUN apk update && apk add nodejs npm

COPY ./react-frontend/package.json ./	 
COPY ./react-frontend/package-lock.json ./	 
COPY ./react-frontend/tsconfig.json ./	 

# install node package dependencies
RUN npm ci

# Copy project files  
COPY ./react-frontend/src ./src
COPY ./react-frontend/public ./public

# Build project
RUN npm run build

# remove dev dependencies	 
RUN npm prune --production
# RUN npm install -g serve

EXPOSE 3000
#ENTRYPOINT ["serve", "-s", "build"]
ENTRYPOINT ["npm", "run", "start"]
