import pandas as pd 
from config import S3_BUCKET
import boto3

def extract_data():
    pdf_files = []

    s3 = boto3.client('s3')
    result = s3.list_objects(Bucket = S3_BUCKET)
    for o in result.get('Contents'):
        data = s3.get_object(Bucket = S3_BUCKET, Key = o.get('Key'))
        body = data['Body'].read() 
        pdf_files.append({
            'key':o.get('key'),
            'body':body
        })
    
    
    
    print('extract done')

    return pdf_files