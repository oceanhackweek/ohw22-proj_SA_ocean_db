from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

#this is use to allow to access the api from a webapp
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], # Allows all origins
	allow_credentials=True,
	allow_methods=["*"], # Allows all methods
	allow_headers=["*"], # Allows all headers
	)

@app.get("/")
def index():
	return {"greeting": "Hello world"}
