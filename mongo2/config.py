

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