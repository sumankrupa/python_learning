

import pandas as pd 
from config import customer_master_path,customer_updates_path

def load_data(final_df, history_df,engine):
    final_df.to_sql(
        name = 'SCD_05',
        con = engine,
        if_exists ='replace'
    )
    history_df.to_sql(
        name = 'Customer_Subscription_History',
        con = engine,
        if_exists ='replace'
    )
    
    print('loading done')
    return 