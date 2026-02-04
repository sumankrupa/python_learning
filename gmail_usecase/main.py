from sqlalchemy import create_engine
import os

from config import connection_string, client_secret_path, SCOPES,TOKEN_PATH
from src.extract import extract
from src.transform import transform
from src.load import load

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build




def get_gmail_service():
    creds = None

    # 1) Load existing token
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # 2) If token missing/invalid, do OAuth login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret_path), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 3) Save token for next run
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    # 4) Build Gmail API service
    service = build("gmail", "v1", credentials=creds)
    return service


def main():
    engine = create_engine(connection_string)

    service = get_gmail_service()
    mails = extract(service, query="in:inbox", max_results=20)
    df = transform(mails)
    
    load(engine, df)


if __name__ == "__main__":
    main()
