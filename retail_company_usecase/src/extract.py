import pandas as pd 
from config import customer_data_path,order_items_data_path,orders_data_path,products_data_path 

def extract_data(engine):
    # 4 csv files
    customer_df = pd.read_csv(customer_data_path)
    order_items_df = pd.read_csv(order_items_data_path)
    orders_data_df = pd.read_csv(orders_data_path)
    products_data_df = pd.read_csv(products_data_path)
    print('extract done')
    return customer_df,order_items_df,orders_data_df,products_data_df