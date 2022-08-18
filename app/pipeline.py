from .fetch_pnboia import *
from .database import *

# collecting the new data from PNBOIA
pnboia_update_local_data()

# TODO: applying the quality control
df = None

# sending data to the database
send_data_to_database(df, tablename='pnboia')
