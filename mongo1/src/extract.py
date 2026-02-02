import json
from typing import List, Dict, Any

from pymongo import MongoClient

from config import  mongo_config,structured_projects_path,unstructured_projects_path

def seed_projects_from_file():
    client = MongoClient(mongo_config["uri"])
    db = client[mongo_config["database"]]
    collection = db[mongo_config["collection"]]

    with open(unstructured_projects_path, "r") as f:
        docs = json.load(f) 

    collection.delete_many({})
    result = collection.insert_many(docs)


# seed_projects_from_file()



def extract(collection):
    documents = list(collection.find({}, {"_id": 0}))
    print('extract done')
    return documents
    