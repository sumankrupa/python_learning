

from pathlib import Path
from urllib.parse import quote_plus



from pathlib import Path

base_dir = Path(__file__).resolve().parent
src_dir = base_dir / "src"

structured_projects_path = src_dir / "../project.txt"
unstructured_projects_path = src_dir / "../Doc_unstructured_1.txt"



mongo_config = {
    "uri": "mongodb://localhost:27017",
    "database": "mydb",
    "collection": "projects"
}

mysql_config = {
    "user": "root",
    "password": "YOURPASS",
    "host": "127.0.0.1",
    "port": 1433,
    "database": "analyticsdb"
}

def mysql_uri():
    return (
        f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}"
        f"@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}"
    )
