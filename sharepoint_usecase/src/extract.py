from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from config import site_url, list_name, client_id, client_secret

def extract():
    ctx = ClientContext(site_url).with_credentials(
        ClientCredential(client_id, client_secret)
    )

    lst = ctx.web.lists.get_by_title(list_name)

    items = (
        lst.items
        .select([
            "Title", "Status", "Project_x0020_Manager",
            "Start_x0020_Date", "End_x0020_Date",
            "Budget", "Department"
        ])
        .get()
        .execute_query()
    )

    rows = []
    for it in items:
        p = it.properties
        rows.append({
            "project_name": p.get("Title"),
            "status": p.get("Status"),
            "project_manager": p.get("Project_x0020_Manager"),
            "start_date": p.get("Start_x0020_Date"),
            "end_date": p.get("End_x0020_Date"),
            "budget": p.get("Budget"),
            "department": p.get("Department"),
        })

    print("extract done")
    return rows
