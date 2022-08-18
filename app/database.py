# -*- coding: utf-8 -*-
import pandas as pd

# load local function
from utils import make_db_connection

def send_data_to_database(df, tablename='pnboia_buoy'):
    """
    Main pipeline to send a dataframe to the database. In this
    function, we also check if there is any duplicated row in the
    database, based on datetime AND pnboia_id. 
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to be uploaded
    tablename : str
        Which table send the data
    """
    # make sure the database won't have duplicated values
    drop_duplicates_from_database(df, tablename=tablename)
    
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