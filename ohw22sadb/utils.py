import os
import sqlalchemy
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
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{os.getenv('POSTGRE_USER')}:{PASS}@{URL}/{os.getenv('POSTGRE_BD')}")
    
    # returning the objects
    return engine
