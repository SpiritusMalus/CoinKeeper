from fastapi import FastAPI
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


@app.post("/create_user/", response_model=UserCreate)
async def create_user(data: UserCreate):
    with get_db() as db:
        hashed_password = pwd_context.hash(data.password)
        new_user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            hashed_password=hashed_password,
        )
        db.session.add(new_user)

    return new_user
