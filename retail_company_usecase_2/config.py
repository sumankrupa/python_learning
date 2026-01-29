from pathlib import Path
from urllib.parse import quote_plus 

base_dir = Path(__file__).resolve().parent
src_dir = base_dir/"src"

customer_data_path = base_dir/"customers_snapshot 1.csv"
dim_customers_path = base_dir/"dim_customers_before 1.csv"



db_config = {
    "user": "sa",
    "password":quote_plus("Suman@2026!SQL"),
    "server":"localhost",
    "database":"marketingdb",
    "driver":"ODBC Driver 18 for SQL Server"
}