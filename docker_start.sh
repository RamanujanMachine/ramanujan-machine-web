#!/bin/bash

# Start the first process
npx vite --host "0.0.0.0" --port 5173 &

# Start the second process
uvicorn main:app --host "0.0.0.0" --port 8000 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?