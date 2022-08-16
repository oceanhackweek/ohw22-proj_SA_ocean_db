import os
import sys
import pandas as pd

HEROKU_TOKEN = 'token=rBx9rZVa7Yi9zNo4U6_M'
PNBOIA_BUOYS_INFO = 'https://remobsapi.herokuapp.com/api/v1/buoys'
PNBOIA_BUOYS_DATA = 'http://remobsapi.herokuapp.com/api/v1/data_buoys'


def pnboia_check_input(input, ids, names):
    """
    Check if input is a valid PNBOIA buoy identifier and if is an id number or name

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
        Message about input, especially important for False isvalid ones

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
    Generate PNBOIA buoy datapath from buoy id number or buoy name

    Parameters
    ----------
    id_or_name : int or str
        Id number or name that identify PNBOIA buoy

    Returns
    -------
        ...
    """
    info_df = pd.read_json(
        PNBOIA_BUOYS_INFO
    )
    isvalid, input_type, msg = pnboia_check_input(
        id_or_name,
        info_df.id.values,
        info_df.name_buoy
    )
    if isvalid:
        if input_type == 'id':
            buoy_id = 'buoy={0}'.format(
                id_or_name
            )
        elif input_type == 'name':
            buoy_id = int(
                info_df.id[
                    info_df.name_buoy.isin([
                        id_or_name
            ])])
            buoy_id = 'buoy={0}'.format(
                buoy_id
            )
        path = (
            PNBOIA_BUOYS_DATA +
            '?' +
            buoy_id +
            '&' +
            HEROKU_TOKEN
        )
    else:
        print(msg)
    
    return path


def pnboia_active_buoys():
    """
    Fetch PNBOIA active buyos

    Returns
    -------
    active_buoys : pandas.DataFrame
        PNBOIA active buoys regarding API status
    """
    info_df = pd.read_json(
        PNBOIA_BUOYS_INFO
    )
    active_buoys = info_df.loc[
        info_df.status == 'Ativa'
    ]

    return active_buoys


def pnboia_download_active_buoys_data():
    """
    Download all available data for each PNBOIA active buoy and save this into individual .csv files on data folder one level above current folder
    """
    scriptdir = os.path.dirname(
        sys.argv[0]
    )
    active_buoys = pnboia_active_buoys()

    for _, buoy in active_buoys.iterrows():
        buoy_name = buoy.name_buoy.strip()
        buoy_name = buoy_name.replace(' ', '_')
        buoy_name = buoy_name.casefold()

        print(
            'Getting {0} data'.format(
                buoy_name.capitalize()
        ))

        buoy_datapath = pnboia_get_datapath(
            buoy.id
        )
        buoy_data = pd.read_json(
            buoy_datapath
        )
        if buoy_data.empty:
            print(
                '..{0} PNBOIA buoy identified as active, but without data from API'.format(
                    buoy_name.capitalize()
            ))
        else:
            buoy_data.to_csv(
                os.path.join(
                    scriptdir,
                    '../data',
                    '{0}.csv'.format(
                        buoy_name
            )))


pnboia_download_active_buoys_data()