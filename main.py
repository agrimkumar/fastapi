from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from models import Gender, User, Role, UserUpdateRequest

app = FastAPI()


db: List[User] = [
    User(
        id=UUID("4d7e9086-5772-4045-be53-b1b43b5659df"),
        first_name="Agrim",
        last_name="Kumar",
        gender=Gender.male,
        roles=[Role.student],
    ),
    User(
        id=UUID("bc504929-be78-460b-a384-fe5175bc9001"),
        first_name="Maria",
        last_name="Williams",
        gender=Gender.female,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
async def root():
    return {"Hello": "Agrim"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"msg": "User deleted"}
    raise HTTPException(
        status_code=404, detail=f"user with id: {user_id} does not exists"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404, detail=f"user with id {user_id} does not exists"
    )
