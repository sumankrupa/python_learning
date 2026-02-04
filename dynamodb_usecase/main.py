from sqlalchemy import create_engine
from pymongo import MongoClient
import boto3
from config import db_config,mongo_config,connection_string,dynamo_config
from src.extract import extract
from src.transform import transform
from src.load import load




def main():
    engine = create_engine(connection_string)
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=dynamo_config["endpoint_url"],
        region_name=dynamo_config["region_name"],
        aws_access_key_id=dynamo_config["aws_access_key_id"],
        aws_secret_access_key=dynamo_config["aws_secret_access_key"],
    )

    records = extract(dynamodb)
    df = transform(records)
    load(engine,df)
    return

if __name__ == "__main__":
    main()
