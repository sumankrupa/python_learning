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
    snap_df,dim_customer_df= extract_data(engine)  
    
    dim_df = transform_data(snap_df,dim_customer_df)
    load_data(dim_df,engine)
    
    


if __name__ == "__main__":
    main()
