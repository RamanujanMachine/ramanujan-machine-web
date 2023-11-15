from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["GET", "POST", "OPTIONS"],
                   allow_credentials=True,
                   allow_headers=["*"])


@app.get("/")
def root():
    content = {"message": "Hello"}
    response = JSONResponse(content=content)
    response.set_cookie(key="trm-cookie", value="fake-cookie-session-value")
    return response
