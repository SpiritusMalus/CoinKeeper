from fastapi import FastAPI
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.schemas.schema import UserLogin, UserRegistration

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI(title="CoinKeeper API")


@app.get("/")
async def main_page():
    return {"lox": "pidr"}


@app.get("/registration/")
async def get_registration_page():
    return {"lox": "pidr"}


@app.post("/registration/", response_model=UserRegistration)
async def post_registration(data: UserRegistration):
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


@app.get("/login/")
async def get_login_page():
    return {"lox": "pidr"}


@app.post("/login/", response_model=UserLogin)
async def post_login_page():
    return {"lox": "pidr"}
