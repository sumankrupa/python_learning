from datetime import datetime

_next_id = 1    # ID counter

def add_task(task_in):
    global _next_id

    out = {
        "id": _next_id,
        "title": task_in["title"].title(),
        "status": task_in["status"].lower(),
        "created_at": datetime.now(),
    }

 
    _next_id += 1

    return out
