
To run the Ramanujan Machine Web Portal backend, make sure that you have python3 and pipenv installed:

python3 -m pip install pipenv

Then execute the following to start the server:

pipenv `uvicorn main:app --reload`

This will launch the API at localhost:8000. 

The API docs will be available at localhost:8000/docs.
