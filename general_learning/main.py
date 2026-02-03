from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Fake in-memory "database"
users = {}

# Data model
class User(BaseModel):
    name: str
    email: str


# GET → Read data
@app.get("/users")
def get_all_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return users[user_id]

# POST → Create data
@app.post("/users/{user_id}")
def create_user(user_id: int, user: User):
    users[user_id] = user
    return {"message": "User created", "data": user}


# PUT → Update data

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    users[user_id] = user
    return {"message": "User updated", "data": user}

# DELETE → Remove data
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    del users[user_id]
    return {"message": "User deleted"}
