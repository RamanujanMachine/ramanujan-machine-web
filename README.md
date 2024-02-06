# Ramanujan Machine Web Portal

## Run with Docker
To run the web portal using the Dockerfile:  

`docker build . -t ramanujan-machine-web-portal:latest`  

`docker run -p 80:5173 -p 127.0.0.1:8000:8000 ramanujan-machine-web-portal:latest`  

Note that the first port is the port you can access via your web browser, e.g. `http://localhost:80` is where you would be able to interact with the app given the above configuration. You can change `80` to whatever port you wish, but the frontend of the web application runs on port `5173` inside the container.

## Run Frontend and Backend Locally without Docker
- Refer to [React Frontend README](./react-frontend/README.md) to run the web interface locally.
- Refer to [Python Backend README](./python-backend/README.md) to run the API locally.
