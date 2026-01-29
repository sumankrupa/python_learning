import pandas as pd 
from config import customer_data_path,dim_customers_path
def extract_data(engine):
    # 4 csv files
    customer_df = pd.read_csv(customer_data_path)
    dim_customer_df = pd.read_csv(dim_customers_path)
    print('extract done')
    return customer_df,dim_customer_df