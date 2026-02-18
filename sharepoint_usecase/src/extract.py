import io
import requests
import pandas as pd
from urllib.parse import urlparse, quote

from config import site_url, tenant_id, client_id, client_secret, csv_path

GRAPH = "https://graph.microsoft.com/v1.0"


def _get_token() -> str:
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default",
    }
    r = requests.post(token_url, data=data, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _get_site_id(token: str) -> str:
    u = urlparse(site_url)
    hostname = u.hostname
    path = u.path.rstrip("/")
    url = f"{GRAPH}/sites/{hostname}:{path}"
    r = requests.get(url, headers=_headers(token), timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def extract() -> pd.DataFrame:
    token = _get_token()
    site_id = _get_site_id(token)

    # Documents library is a drive in Graph
    drive = requests.get(f"{GRAPH}/sites/{site_id}/drive", headers=_headers(token), timeout=30)
    drive.raise_for_status()
    drive_id = drive.json()["id"]

    item_path = quote(csv_path)
    content_url = f"{GRAPH}/drives/{drive_id}/root:/{item_path}:/content"

    resp = requests.get(content_url, headers=_headers(token), timeout=60)
    resp.raise_for_status()

    df = pd.read_csv(io.BytesIO(resp.content))
    print("extract done:", df.shape)
    return df
