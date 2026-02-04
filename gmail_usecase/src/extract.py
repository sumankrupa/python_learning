import json
import base64

from pymongo import MongoClient

from config import  mongo_config,structured_projects_path,unstructured_projects_path

def get_header(headers, name):
    name = name.lower()
    for h in headers:
        if h.get("name", "").lower() == name:
            return h.get("value", "")
    return ""


def get_body(payload):
    def decode(data):
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # Simple (non-multipart) email
    if "parts" not in payload:
        body = payload.get("body", {}).get("data")
        return decode(body) if body else ""

    # Multipart (simple version): try to find text/plain
    for part in payload["parts"]:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            return decode(data) if data else ""

    # fallback html
    for part in payload["parts"]:
        if part.get("mimeType") == "text/html":
            data = part.get("body", {}).get("data")
            return decode(data) if data else ""

    return ""


def get_attachments(payload):
    names = []

    # ✅ No parts => no attachments
    if "parts" not in payload:
        return names

    for part in payload["parts"]:
        filename = part.get("filename")
        if filename:           # ✅ only if not "" / None
            names.append(filename)

    return names



def extract(service,query, max_results):
    resp = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    msgs = resp.get("messages", []) or []
    

    records = []
    for i in msgs:
        # get full message for each id
        msg = service.users().messages().get(
            userId='me',
            id=i["id"],
            format="full"
        ).execute()
        payload = msg.get("payload", {}) or {}
        headers = payload.get("headers",[]) or []
 
        records.append({
                "Sender": get_header(headers, "From"),
                "Receiver": get_header(headers, "To"),
                "CC": get_header(headers, "Cc"),
                "Subject": get_header(headers, "Subject"),
                "Body": get_body(payload),
                "Attachments": ", ".join(get_attachments(payload)),
            })
    print('extract done')
    return records