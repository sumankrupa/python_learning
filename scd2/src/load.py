

import pandas as pd 
from config import customer_master_path,customer_updates_path

def load_data(final_df,engine):
    final_df.to_sql(
        name = 'SCD_02',
        con = engine,
        if_exists = 'replace',
        index = False
    )
    print(final_df,'loading done')
    return 