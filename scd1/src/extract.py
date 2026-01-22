import pandas as pd 
from config import customer_master_path, customer_updates_path 

def extract():
    master_df = pd.read_csv(customer_master_path)
    update_df = pd.read_csv(customer_updates_path)
    print('extract done')
    return master_df, update_df