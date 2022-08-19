import pandas as pd
import requests


def get_list_pnboia(url=None):
    """
    return a dataframe containing a list with available buoys from PNBOIA
    """
    query = f'{url}/metadata/pnboia'
    
    request = requests.get(query)
    return pd.DataFrame(request)    
    

def get_pnboia(kwargs, url=None):
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
    ds = pd.DataFrame(data).to_dataset()
    
    for key,value in metadata.items():
        ds.attrs[key] = value
    
    return ds


def build_query(kwargs, API_URL='url'):
    """
    """
    # bulding the metadata query
    if pnboia_id in kwargs.keys():
        # query a specific buoy
        pnboia_id = kwargs['pnboia_id']
        query_metadata = f"{API_URL}/metadata/pnboia/?buoy_id={pnboia_id}"
    else:
        raise ValueError("Please, provide a valid buoy_id.")
        
   # building the data query
    query = f"{API_URL}/buoy/?"   
    for key,value in kwargs.items():
        query += f"{key}={value}&"
    
    # querying the metadata for a specific buoy
    metadata = requests.get(query_metadata)
    # querying the data itself
    data = requests.get(query)
        
    return data, metadata