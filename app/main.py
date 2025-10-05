from fastapi import Depends, FastAPI, Form, Request
from passlib.context import CryptContext
import redis
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from services.email.imap_service import EmailImapService
from services.email.smtp_service import EmailSmtpService
from config.config import REDIS_HOST, REDIS_PORT, EMAIL_ADDRESS
from database import get_db_dependency
from models.user import User
from schemas.user_schema import UserLogin, UserRegistration

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
    await EmailImapService().load_emails()
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
    request: Request,
    db: AsyncSession = Depends(get_db_dependency),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...),
) -> "RedirectResponse":
    form_data = UserRegistration(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        repeat_password=repeat_password,
    )

    hashed_password = pwd_context.hash(form_data.password)

    exists_query = select(exists().where(User.email == form_data.email))
    result = await db.execute(exists_query)
    user_exists = result.scalar()

    if user_exists:
        return templates.TemplateResponse(
            "auth/registration/registration.html",
            {
                "request": request,
                "data": {
                    "first_name": form_data.first_name,
                    "last_name": form_data.last_name,
                    "email": form_data.email,
                },
                "error": "Пользователь с таким email уже существует",
            },
        )

    db.add(
        User(
            first_name=form_data.first_name,
            last_name=form_data.last_name,
            email=form_data.email,
            hashed_password=hashed_password,
        )
    )

    with open(
        "./templates/auth/registration/accept_registration.html", "r", encoding="utf-8"
    ) as file:
        html_content = file.read()

    await EmailSmtpService().send_email(
        sender=EMAIL_ADDRESS,
        to_email=email,
        subject="Подтверждение регистрации CoinKeeper",
        body=html_content,
        is_html=True,
    )

    return RedirectResponse("/login/", status_code=303)  ### ВЫНЕСТИ ВСЁ В КЛАСС + DI


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
