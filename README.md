# Ramanujan Machine Web Portal

## Run with Docker
To run the web portal using the Dockerfile:  

`docker build . -t ramanujan-machine-web-portal:latest`  

`docker run -p 8080:3000 ramanujan-machine-web-portal:latest`  

Note that the first port is the port you can access via your web browser, e.g. `http://localhost:8080` is where you would be able to interact with the app given the above configuration. You can change `8080` to whatever port you wish, but the application runs on port `3000` inside the container.

## Run with Docker
Refer to [React Frontend README](./react-frontend/README.md) to run locally.
