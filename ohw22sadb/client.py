import pandas as pd
import requests


def get_list_pnboia(url='http://sadbapi.herokuapp.com'):
    """
    return a dataframe containing a list with available buoys from PNBOIA
    """
    query = f'{url}/metadata/pnboia'
    
    request = requests.get(query)
    df = pd.json_normalize(request.json())
    
    return df
    

def get_pnboia(kwargs, url='http://sadbapi.herokuapp.com'):
    """
    Get data based on kwargs dictionary, which contains the parameters
    to perform a query.
    
    Parameters
    ----------
    kwargs : dict
        Dictionary containing the query parameters.
    
    Returns
    -------
    ds : xarray.Dataset
        Dataset containing the return of the query along with metadata
    """
    # building and querying the data and metadata
    data, metadata = build_query(kwargs, url=url)
    
    # converting the API returns into Dataset with metadata
    df = pd.json_normalize(data.json())
    df.set_index('datetime', inplace=True)
    
    # dropping some columns
    df = df.drop(columns=['pnboia_id'])
    
    ds = df.to_xarray()
    
    for key,value in metadata.json()[0].items():
        ds.attrs[key] = value
    
    return ds


def build_query(kwargs, url='http://sadbapi.herokuapp.com'):
    """
    """
    # bulding the metadata query
    if 'buoy_id' in kwargs.keys():
        # query a specific buoy
        buoy_id = kwargs['buoy_id']
        query_metadata = f"{url}/metadata/pnboia/?buoy_id={buoy_id}"
        
        # query the data
        query = f"{url}/buoy/{buoy_id}/?"
        for key,value in kwargs.items():
            query += f"{key}={value}&"
   
        # querying the metadata for a specific buoy
        metadata = requests.get(query_metadata)
        # querying the data itself
        data = requests.get(query)
        
    else:
        raise ValueError("Please, provide a valid buoy_id.")
          
    return data, metadata