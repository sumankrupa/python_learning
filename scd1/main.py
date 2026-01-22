from config import db_config
from sqlalchemy import create_engine
from src.extract import extract
from src.transform import transform
from src.load import load 


connection_string = (
    f"mssql+pyodbc://{db_config['user']}:{db_config['password']}"
    f"@{db_config['server']}/{db_config['database']}"
    f"?driver={db_config['driver'].replace(' ', '+')}"
    "&Encrypt=no"

)
engine = create_engine(connection_string)

def main():
    master_df,update_df = extract()
    final_df = transform(master_df, update_df)
    load(final_df, engine)
    print('etl done')
    



if __name__ == "__main__":
    main()
