import requests
from config import token_url,token_payload,sf_api_version, get_token

def extract_data(limit: int = 200):
   

    access_token,instance_url = get_token()

    # 2) Query Accounts
    soql = (
        "SELECT Id, Name, Industry, Type, BillingCity, BillingState, "
        "CreatedDate, LastModifiedDate "
        "FROM Account "
        "ORDER BY LastModifiedDate DESC "
        f"LIMIT {int(limit)}"
    )

    query_url = f"{instance_url}/services/data/{sf_api_version}/query"
    print(query_url)


    resp = requests.get(
        query_url,
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        params={"q": soql},
        timeout=30,
    )

    if resp.status_code >= 400:
        raise RuntimeError(f"Salesforce QUERY ERROR {resp.status_code}: {resp.text}")

    data = resp.json()
    records = data.get("records")

    for r in records:
        r.pop("attributes", None)
    print('extract done')
    return records

