

from pathlib import Path
from urllib.parse import quote_plus



from pathlib import Path

base_dir = Path(__file__).resolve().parent
src_dir = base_dir / "src"

structured_projects_path = src_dir / "../project.txt"
unstructured_projects_path = src_dir / "../Doc_unstructured_1.txt"



mongo_config = {
    "uri": "mongodb://localhost:27017",
    "database": "local",
    "collection": "projects"
}


db_config = {
    "user": "sa",
    "password":quote_plus("Suman@2026!SQL"),
    "server":"localhost:1433",
    "database":"marketingdb",
    'port':1433,
    "driver":"ODBC Driver 18 for SQL Server"
   
}
dynamo_config = {
        "endpoint_url": "http://localhost:8000",
        "region_name": "us-east-1",
        "aws_access_key_id": "test",
        "aws_secret_access_key": "test"
    }



connection_string = (
    f"mssql+pyodbc://{db_config['user']}:{db_config['password']}"
    f"@{db_config['server']}/{db_config['database']}"
    f"?driver={db_config['driver'].replace(' ', '+')}"
    "&Encrypt=no"

)



SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

client_secret_path = base_dir / "client_secret.json"  
TOKEN_PATH = base_dir / "token.json"  
