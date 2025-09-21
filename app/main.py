from fastapi import Depends, FastAPI, Form, Request
from passlib.context import CryptContext
import redis
from sqlalchemy.ext.asyncio import AsyncSession
from config.config import REDIS_HOST, REDIS_PORT
from database import get_db_dependency
from models.user import User
from schemas.schema import UserLogin, UserRegistration

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="CoinKeeper API")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настройка Jinja2
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "CoinKeeper - Главная"}
    )


@app.get("/registration/")
async def get_registration_page(request: Request):
    return templates.TemplateResponse(
        "auth/registration/registration.html",
        {"request": request, "title": "CoinKeeper - Регистрация"},
    )


@app.post("/registration/")
async def post_registration(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...),
    db: AsyncSession = Depends(get_db_dependency),
) -> "RedirectResponse":
    form_data = UserRegistration(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        repeat_password=repeat_password,
    )

    hashed_password = pwd_context.hash(form_data.password)

    new_user = User(
        first_name=form_data.first_name,
        last_name=form_data.last_name,
        email=form_data.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)

    return RedirectResponse("/login/", status_code=303)


@app.get("/login/")
async def get_login_page(request: Request, after_registration: bool = False):
    return templates.TemplateResponse(
        "auth/login/login.html",
        {
            "request": request,
            "title": "CoinKeeper - Логин",
            "after_registration": after_registration,
        },
    )


@app.post("/login/", response_model=UserLogin)
async def post_login_page():
    return {"lox": "pidr"}
