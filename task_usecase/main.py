from fastapi import FastAPI
from typing import List
from .models import TaskOut, TaskIn
from .models_api import add_task

app = FastAPI(title="Task Usecase")

@app.post("/tasks", response_model=List[TaskOut])
def create_task(payload: List[TaskIn]):
    tasks = []
    for task in payload:
        tasks.append(add_task(task.dict()))
    return tasks
