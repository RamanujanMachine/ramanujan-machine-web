#!/bin/bash

# Start gRPC server
cd lirec-grpc-server
. venv/bin/activate
python server.py &
deactivate
cd ..

# Start the web server
cd python-backend
. venv/bin/activate
uvicorn main:app --host "0.0.0.0" --port 80 &
deactivate

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?