from dotenv import load_dotenv
import os

from schemas.email_schema import Settings

# Загружаем переменные окружения
load_dotenv()

### MAIN
MAIN_URL = os.environ.get("MAIN_URL")

### DATABASE
DATABASE_URL = os.environ.get("DATABASE_URL")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

### COOKIE
LOGIN_TO_ACCOUNT = os.environ.get("LOGIN_TO_ACCOUNT")
RESET_PASS_ACCOUNT = os.environ.get("RESET_PASS_ACCOUNT")
REGISTER_ACCOUNT = os.environ.get("REGISTER_ACCOUNT")

### REDIS
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

### EMAIL
EMAIL_SETTINGS = Settings()
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
