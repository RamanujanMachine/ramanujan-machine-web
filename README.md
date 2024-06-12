# Ramanujan Machine Web Portal

## Run with Docker
To run the web portal using the Dockerfile:  

`docker build --build-arg wolfram_app_id=XXXXXX-XXXXXXXXXX --build-arg public_ip=localhost . -t ramanujan-machine-web-portal:latest`  

You will need to replace `XXXXXX-XXXXXXXXXX` with a Wolfram App Id, which you can obtain from Wolfram [here](https://developer.wolframalpha.com/).

`docker run -p 80:80 ramanujan-machine-web-portal:latest`  

Note that the first port is the port you can access via your web browser, e.g. `http://localhost:80` is where you would be able to interact with the app given the above configuration. You can change `80` to whatever port you wish, and the frontend of the web application runs on port `80` inside the container.

## Run Frontend and Backend Locally without Docker
Comprehensive developer documentation is available in a separate [README](./docs/DEVELOPER.md). Short versions of the instructions for each part of the web app can be found in READMEs in each subdirectory:
- Refer to [React Frontend README](./react-frontend/README.md) to run the web interface locally.
- Refer to [Python Backend README](./python-backend/README.md) to run the API locally.
- Refer to [Python gRPC Server README](./lirec-grpc-server/README.md) to run the gRPC server locally.
