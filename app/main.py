import json
from typing import Any
import uuid
from fastapi import Depends, FastAPI, Form, Request
from passlib.context import CryptContext
import redis
from config.config import REDIS_HOST, REDIS_PORT
from database import get_db
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


# Решить вопрос с редисом. Остановился на том, что я хочу после регистрации класть в редис ключ и доставать его сразу из логина попом
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # Получаем session_id из cookie или создаем новый
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session_data = {}
    else:
        # Достаем данные из Redis
        redis_data = redis_client.get(f"session:{session_id}")
        session_data = json.loads(redis_data) if redis_data else {}

    # Добавляем сессию в запрос
    request.state.session = session_data

    # Передаем запрос дальше
    response = await call_next(request)

    # Сохраняем сессию в Redis
    redis_client.setex(
        f"session:{session_id}",
        3600,  # 1 час
        json.dumps(session_data),
    )

    # Устанавливаем cookie
    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        max_age=3600,
        secure=False,  # True для production
    )

    return response


# Зависимость для удобного доступа к сессии
def get_session(request: Request) -> dict[str, Any]:
    return request.state.session


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request, session: dict[str, Any] = Depends(get_session)):
    print(request.state.session)
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
) -> "RedirectResponse":
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
