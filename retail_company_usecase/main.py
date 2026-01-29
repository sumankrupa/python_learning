from config import db_config 
from sqlalchemy import create_engine 
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

connection_string = (
    f"mssql+pyodbc://{db_config['user']}:{db_config['password']}"
    f"@{db_config['server']}/{db_config['database']}"
    f"?driver={db_config['driver'].replace(' ', '+')}"
    "&Encrypt=no"

)
engine = create_engine(connection_string)
def main():
    # SCD_01 is masterdf
    customer_df,order_items_df,orders_data_df,products_data_df = extract_data(engine)  
    
    line, order_level, region_month = transform_data(customer_df,order_items_df,orders_data_df,products_data_df)
    load_data(line, order_level, region_month,engine)
    
    


if __name__ == "__main__":
    main()
