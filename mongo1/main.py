from sqlalchemy import create_engine
from pymongo import MongoClient
import json
from config import mysql_uri, mongo_config
from src.extract import extract
from src.transform import transform
from src.load import load



def main():
    # Mongo connect
    client = MongoClient(mongo_config["uri"])
    db = client[mongo_config["database"]]
    collection = db[mongo_config["collection"]]

    
    data = extract(collection)

    project_df,project_technologies_df,project_team_members_df,project_milestones_df = transform(data)

    engine = create_engine(mysql_uri())
   
    load(engine, project_df,project_technologies_df,project_team_members_df,project_milestones_df)

    print("ETL done")


if __name__ == "__main__":
    main()
