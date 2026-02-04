

from pydantic import BaseModel, Field 
from datetime import datetime

class TaskIn(BaseModel):
    title:str
    status:str

class TaskOut(BaseModel):
    id:int
    title:str 
    status:str
    created_at:datetime