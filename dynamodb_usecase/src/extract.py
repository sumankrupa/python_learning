import json


from pymongo import MongoClient

from config import  mongo_config,structured_projects_path,unstructured_projects_path




def extract(dynamodb):
    table = dynamodb.Table("CustomerMaster")
    resp = table.scan()
    records = resp.get("Items", [])
    while "LastEvaluatedKey" in resp:
        resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
        records.extend(resp.get("Items", []))
    print('extract done')
    
    return records
    