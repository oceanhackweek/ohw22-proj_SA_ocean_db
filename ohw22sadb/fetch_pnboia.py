# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BUOYS_INFO = pd.read_json(
    os.environ['PNBOIA_BUOYS_INFO']
)

def pnboia_check_input(input, ids, names):
    """
    Check if input is a valid PNBOIA buoy identifier and if
    is an id number or name

    Parameters
    ----------
    input : int or str
        Id number or name that identify PNBOIA buoy
    ids : array
        Possible buoy id number values
    names : pandas.Series
        Possible buoy names with exactly spelling

    Returns
    -------
    isvalid : bool
        Define if input is valid
    input_type : str
        Say if input is buoy id number or buoy name
    msg : str
        Message about input, especially important for False
        isvalid ones

    """
    broad_msg = 'input should be buoy id number or buoy name'
    try:
        obj = int(float(input))
        input_type = 'id'

        if obj > 0 and obj <= ids.max():
            isvalid = True
            msg = 'id value was between 0 and {0}'.format(
                ids.max()
            )
        else:
            isvalid = False
            msg = 'id value should be between 0 and {0}'.format(
                ids.max()
            )
    except ValueError:
        if input:
            input_type = 'name'
            
            if any(names.isin([input])):
                isvalid = True
                msg = 'buoy name is valid'
            else:
                isvalid = False
                msg = 'buoy name should be one of {0}'.format(
                    list(names.values)
                )
        else:
            isvalid = False
            input_type = 'empty'
            msg = '{0}, not an empty string'.format(
            broad_msg
            )
    except TypeError:
        isvalid = False
        input_type = type(input)
        msg = '{0}, not a {1}'.format(
            broad_msg,
            input_type
        )

    return isvalid, str(input_type), msg


def pnboia_get_datapath(id_or_name):
    """
    Generate PNBOIA buoy datapath from buoy id number or
    buoy name

    Parameters
    ----------
    id_or_name : int or str
        Id number or name that identify PNBOIA buoy

    Returns
    -------
        ...
    """
    isvalid, input_type, msg = pnboia_check_input(
        id_or_name,
        BUOYS_INFO.id.values,
        BUOYS_INFO.name_buoy
    )
    if isvalid:
        if input_type == 'id':
            buoy_id = 'buoy={0}'.format(
                id_or_name
            )
        elif input_type == 'name':
            buoy_id = int(
                BUOYS_INFO.id[
                    BUOYS_INFO.name_buoy.isin([
                        id_or_name
            ])])
            buoy_id = 'buoy={0}'.format(
                buoy_id
            )
        path = (
            os.environ['PNBOIA_BUOYS_DATA'] +
            '?' +
            buoy_id +
            '&' +
            os.environ['HEROKU_TOKEN']
        )
    else:
        print(msg)
    
    return path


def pnboia_seek_active_buoy():
    """
    Seek for PNBOIA's active buoys

    Returns
    -------
    active_buoys : pandas.DataFrame
        PNBOIA's active buoys regarding API status
    """
    active_buoys = BUOYS_INFO.loc[
        BUOYS_INFO.status == 'Ativa'
    ]

    return active_buoys


def pnboia_get_active_buoy_data(buoy_id):
    """
    Get all available data for each active buoy

    Returns
    -------
    data_dict : dict
        Dictionary where key is active buoy name and value
        is its data stored into a pandas.DataFrame
    """
    active_buoys = pnboia_seek_active_buoy()

    if any(active_buoys.id.isin([buoy_id])):

        buoy_name = active_buoys.name_buoy[
            active_buoys.id == buoy_id
        ].values[0]

        buoy_datapath = pnboia_get_datapath(
            buoy_id
        )
        buoy_data = pd.read_json(
            buoy_datapath
        )
        if buoy_data.empty:
            print(
                '..{0} buoy is identified as active, but API returns an empty query'.format(
                    buoy_name.capitalize()
            ))
        else:
            buoy_data.set_index(
                'date_time',
                drop=True,
                inplace=True
            )
    
            return buoy_data
