from sqlalchemy import create_engine
from pymongo import MongoClient
import json
from config import db_config,mongo_config
from src.extract import extract
from src.transform import transform
from src.load import load



def seed_projects_from_file():
    client = MongoClient(mongo_config["uri"])
    db = client[mongo_config["database"]]
    collection = db[mongo_config["collection"]]

    with open(unstructured_projects_path, "r") as f:
        docs = json.load(f)

    collection.delete_many({})
    result = collection.insert_many(docs)

# seed_projects_from_file()

connection_string = (
    f"mssql+pyodbc://{db_config['user']}:{db_config['password']}"
    f"@{db_config['server']}/{db_config['database']}"
    f"?driver={db_config['driver'].replace(' ', '+')}"
    "&Encrypt=no"

)
engine = create_engine(connection_string)

def main():
    # Mongo connect
    client = MongoClient(mongo_config["uri"])
    db = client[mongo_config["database"]]
    collection = db[mongo_config["collection"]]

    
    data = extract(collection)

    project_df,project_technologies_df,project_team_members_df,project_milestones_df = transform(data)

    print("BEFORE LOAD")
    load(engine, project_df, project_technologies_df, project_team_members_df, project_milestones_df)
    print("AFTER LOAD")
    return



if __name__ == "__main__":
    main()
