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
    master_df,update_df = extract_data(engine)  
    
    final_df, history_df = transform_data(master_df,update_df)
    load_data(final_df,history_df,engine)
    
    


if __name__ == "__main__":
    main()
