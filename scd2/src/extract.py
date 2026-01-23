
import pandas as pd 
from config import customer_master_path,customer_updates_path
def extract_data(engine):
    master_df = pd.read_sql('select * from dbo.SCD_01',engine)
    update_df = pd.read_csv(customer_updates_path)
    print('extract done')
    return master_df, update_df

    