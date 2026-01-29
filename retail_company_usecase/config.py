from pathlib import Path
from urllib.parse import quote_plus 

base_dir = Path(__file__).resolve().parent
src_dir = base_dir/"src"

customer_data_path = base_dir/"customers 1.csv"
order_items_data_path = base_dir/"order_items 1.csv"
orders_data_path = base_dir/"orders 1.csv"
products_data_path = base_dir/"products 1.csv"


db_config = {
    "user": "sa",
    "password":quote_plus("Suman@2026!SQL"),
    "server":"localhost",
    "database":"marketingdb",
    "driver":"ODBC Driver 18 for SQL Server"
}