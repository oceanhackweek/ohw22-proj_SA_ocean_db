from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Union
import pandas as pd
from dotenv import load_dotenv
import sqlalchemy
import os

def make_db_connection():
	# reading credentials
	load_dotenv()

	PASS = os.getenv('POSTGRE_PWD')
	URL = os.getenv('POSTGRE_LOCAL')

	# creating an engine with sqlalchemy
	engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{os.getenv('POSTGRE_USER')}:{PASS}@{URL}/{os.getenv('POSTGRE_BD')}")
	# returning the objects
	return engine

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

@app.get("/test")
def index():
	df = pd.read_csv('/home/jovyan/OHW22_SA_ocean_db/api/abrolhos.csv')
	df = df.to_json()
	return df


@app.get("/buoy/{buoy_id}/")
def read_buoy(buoy_id: int, 
			  vars: Union[str, None] = None, 
			  start_date: Union[str, None] = None, 
			  final_date: Union[str, None] = None):

	engine = make_db_connection()

	criteria = []
	# datetime
	if start_date:
		query_date_start = f''' datetime >= '{start_date}' '''
		criteria.append(query_date_start)

	if final_date:
		query_date_final = f''' datetime <= '{final_date}' '''
		criteria.append(query_date_final)

	# variaveis do banco
	if type(vars) == str:
		query = f''' SELECT datetime, {str(vars)}, obsv_id FROM pnboia '''
	elif type(vars) == list:
		query = f''' SELECT datetime, {str(vars)[1:-1]}, obsv_id FROM pnboia '''

	else:
		query = f''' SELECT * FROM pnboia '''

	if len(criteria) > 1:
		# loop
		query += f''' WHERE {criteria[0]} '''
		
		for c in criteria[1:]:
			query += f''' AND {c}'''
	elif len(criteria) == 0:
		query += ''
	else:
		query += f''' WHERE {criteria[0]} '''

	df = pd.read_sql_query(query, con=engine)

	df.drop(columns=['obsv_id'], inplace=True)
	df = df.fillna(-9999)

	result = df.to_dict(orient="records")

	return result
