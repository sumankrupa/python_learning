from pathlib import Path
from urllib.parse import quote_plus 

base_dir = Path(__file__).resolve().parent
src_dir = base_dir/"src"

customer_master_path = base_dir.parent/"Customer_Master.csv"
customer_updates_path = base_dir.parent/"Customer_Updates.csv"


db_config = {
    "user": "sa",
    "password":quote_plus("Suman@2026!SQL"),
    "server":"localhost",
    "database":"marketingdb",
    "driver":"ODBC Driver 18 for SQL Server"
}