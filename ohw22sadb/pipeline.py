from ohw22sadb.fetch_pnboia import *
from ohw22sadb.database import *
from ohw22sadb.qartod import run_qc
from ohw22sadb.utils import make_db_connection

# collecting the new data from PNBOIA
print("Updating local file with the last data from PNBOIA")
pnboia_update_local_data()

# getting active buoys list from the database
engine = make_db_connection()

query = f''' SELECT pnboia_id,fname FROM ohw_satlantic.pnboia_buoy_metadata WHERE status = 1 '''
buoys = pd.read_sql_query(query, con=engine)['fname'].to_list()

for buoy in buoys:
    # applying quality control pipeline for each active PNBOIA
    df = run_qc(buoy)

    # sending data to the database
    send_data_to_database(df, tablename='pnboia')