from fastapi import FastAPI, Form, Request
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.schemas.schema import UserLogin, UserRegistration

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI(title="CoinKeeper API")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настройка Jinja2
templates = Jinja2Templates(directory="templates")


# Пишу для себя. 2 Варианта. Сделать тут всё через класс и регистрировать роутеры. Либо Сделать return class.run() или типа того
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


# @app.post("/registration/", response_model=UserRegistration)
# async def post_registration(data: UserRegistration):
#     print(data)
#     with get_db() as db:
#         hashed_password = pwd_context.hash(data.password)
#         new_user = User(
#             first_name=data.first_name,
#             last_name=data.last_name,
#             email=data.email,
#             hashed_password=hashed_password,
#         )
#         db.session.add(new_user)

#     return new_user


@app.post("/registration/")
async def post_registration(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...),
):
    form_data = UserRegistration(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        repeat_password=repeat_password,
    )
    with get_db() as db:
        hashed_password = pwd_context.hash(form_data.password)
        new_user = User(
            first_name=form_data.first_name,
            last_name=form_data.last_name,
            email=form_data.email,
            hashed_password=hashed_password,
        )
        db.add(new_user)
    print(form_data)
    return RedirectResponse("/", status_code=303)


@app.get("/login/")
async def get_login_page():
    return {"lox": "pidr"}


@app.post("/login/", response_model=UserLogin)
async def post_login_page():
    return {"lox": "pidr"}
