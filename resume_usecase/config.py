from pathlib import Path
from urllib.parse import quote_plus


base_dir = Path(__file__).resolve().parent
src_dir = base_dir/"src"




db_config = {
    "user": "sa",
    "password":quote_plus("Suman@2026!SQL"),
    "server":"localhost",
    "database":"marketingdb",
    "driver":"ODBC Driver 18 for SQL Server"
}


connection_string = (
    f"mssql+pyodbc://{db_config['user']}:{db_config['password']}"
    f"@{db_config['server']}/{db_config['database']}"
    f"?driver={db_config['driver'].replace(' ', '+')}"
    "&Encrypt=no"

)

import os

# s3 settings
S3_BUCKET = "etl-suman-files"
S3_INCOMING_PREFIX = ""        # PDFs are directly in bucket
S3_ARCHIVE_PREFIX = "archive/"
S3_FAILED_PREFIX = "failed/"
AWS_REGION = "us-east-2"