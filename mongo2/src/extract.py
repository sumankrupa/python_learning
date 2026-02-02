import json
from typing import List, Dict, Any

from pymongo import MongoClient

from config import  mongo_config,structured_projects_path,unstructured_projects_path




def extract(collection):
    documents = list(collection.find({}, {"_id": 0}))
    print('extract done')
    return documents
    