from urllib.parse import quote_plus

# SharePoint
site_url = "https://kasmoco.sharepoint.com/sites/kasmo-training"
list_name = "Project_details"



client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"


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


