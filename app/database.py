# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import pandas as pd
import sqlalchemy
from urllib.parse import quote  

from dotenv import load_dotenv


def make_db_connection():
    """
    Create a connection with the database, using environment variables available.
    
    Parameters
    ----------
    
    Returns
    -------
    engine : sqlalchemy.engine.base.Engine
        engine used to communicate with the database
    """
    # reading credentials
    load_dotenv()
        
    PASS = os.getenv('POSTGRE_PWD')
    URL = os.getenv('POSTGRE_LOCAL')
    
    # creating an engine with sqlalchemy
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{os.getenv('POSTGRE_USER')}:{quote(PASS)}@{URL}/{os.getenv('POSTGRE_BD')}")
    
    # returning the objects
    return engine

# TODO: just an old function used to test the database. Can be deleted upon acceptation to merge
# def read_csv_temporarily(buoy_id=27):
#     """
#     just a dummy function that reads a csv file and send the data
#     to the database
#     """
#     df = pd.read_csv('../data/alcatrazes.csv')
    
#     # sorting data
#     df = df.sort_values('date_time')
    
#     # selecting columns
#     df_sql = df[['buoy_id', 'date_time', 'swvht1', 'tp1', 'wvdir1']]
    
#     engine = make_db_connection()
    
#     df_sql = df_sql.rename({'buoy_id': 'pnboia_id',
#                             'date_time': 'datetime', 
#                             'swvht1': 'wvht', 
#                             'tp1': 'tp', 
#                             'wvdir1': 'wvdir'}, axis=1)
    
#     df_sql.index = df_sql.index.rename('obsv_id')
    
#     df_sql.to_sql(con=engine, name='pnboia_buoy', if_exists='append', index=False)
    
   
def send_data_to_database(df, tablename='pnboia_buoy'):
    """
    
    """
    # get credentials
    engine = make_db_connection()
    
    # saving data into the database
    df.to_sql(con=engine, name=tablename, if_exists='append', index=False)
    

def drop_duplicates_from_database(df, tablename='pnboia_buoy'):
    """
    auxiliar function to delete any duplicated observation from the database,
    based on the pnboia_buoy and datetime.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with valid data to check for duplicates
    tablename : str
        Which table name we must to check
    
    Returns
    -------
    """
    
    # listing all dates we want to remove from the database if exist
    dates_to_delete = [pd.to_datetime(d).strftime('%Y-%m-%d %H:%M:00') for d in df['datetime'].unique()]
    # listing all pnboia buoys to do the same
    buoys = df['pnboia_id'].unique()
    
    # now creating a query to delete rows from the database based
    # on two conditions: if datetime is in our dates list and if 
    # pnboia_id is in our buoys list
    del_query = f'''
                    DELETE FROM {tablename} 
                    WHERE 
                        datetime in ({str(dates_to_delete)[1:-1]})
                    AND
                        pnboia_id in ({str(buoys)[1:-1]})
                 '''
                 
    # now connecting with the database
    engine = make_db_connection()
    
    # running our delete query
    with engine.begin() as conn:
        conn.execute(del_query)