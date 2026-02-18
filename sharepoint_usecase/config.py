from urllib.parse import quote_plus

# SharePoint
site_url = "https://kasmoco.sharepoint.com/sites/kasmo-training"
csv_path = "Shared Documents/sumandhara/order_data.csv"


tenant_id = "979ffdff-332b-406c-8644-6d8db569225f"
client_id = "PUT-GUID-HERE"
client_secret = "PUT-SECRET-HERE"


username = "sumandhara.krupanidhi@kasmodigital.com"
password = "SuperBoof@98"

# SQL Server
db_config = {
    "user": "sa",
    "password": quote_plus("Suman@2026!SQL"),
    "server": "localhost:1433",
    "database": "marketingdb",
    "driver": "ODBC Driver 18 for SQL Server",
}

connection_string = (
    f"mssql+pyodbc://{db_config['user']}:{db_config['password']}"
    f"@{db_config['server']}/{db_config['database']}"
    f"?driver={db_config['driver'].replace(' ', '+')}"
    "&Encrypt=no"
)


