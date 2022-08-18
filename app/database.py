# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import pandas as pd
import sqlalchemy
from urllib.parse import quote  

from datetime import datetime
from dotenv import load_dotenv


def make_db_connection():
    # reading credentials
    load_dotenv()
        
    PASS = os.getenv('POSTGRE_PWD')
    URL = os.getenv('POSTGRE_LOCAL')
    
    # creating an engine with sqlalchemy
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{os.getenv('POSTGRE_USER')}:{quote(PASS)}@{URL}/{os.getenv('POSTGRE_BD')}")
    
    # returning the objects
    return engine


def read_csv_temporarily(buoy_id=27):
    
    df = pd.read_csv('../data/alcatrazes.csv')
    
    # sorting data
    df = df.sort_values('date_time')
    
    # selecting columns
    df_sql = df[['buoy_id', 'date_time', 'swvht1', 'tp1', 'wvdir1']]
    
    engine = make_db_connection()
    
    df_sql = df_sql.rename({'buoy_id': 'pnboia_id',
                            'date_time': 'datetime', 
                            'swvht1': 'wvht', 
                            'tp1': 'tp', 
                            'wvdir1': 'wvdir'}, axis=1)
    
    df_sql.index = df_sql.index.rename('obsv_id')
    
    df_sql.to_sql(con=engine, name='pnboia_buoy', if_exists='append', index=False)
    
   
def send_data_to_database(df, tablename='pnboia_buoy'):
    
    # get credentials
    engine = make_db_connection()
    
    # saving data into the database
    df.to_sql(con=engine, name=tablename, if_exists='append', index=False)