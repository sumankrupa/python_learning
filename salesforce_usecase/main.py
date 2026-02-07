from sqlalchemy import create_engine
from config import db_config
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
    records = extract_data( limit=200)
    df = transform_data(records)

   
    engine = create_engine(connection_string, echo=False)
    load_data(engine, df)


if __name__ == "__main__":
    main()
