from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

### MAIN
MAIN_URL = os.environ.get("MAIN_URL")

### DATABASE
DATABASE_URL = os.environ.get("DATABASE_URL")

### COOKIE
LOGIN_TO_ACCOUNT = os.environ.get("LOGIN_TO_ACCOUNT")
RESET_PASS_ACCOUNT = os.environ.get("RESET_PASS_ACCOUNT")
REGISTER_ACCOUNT = os.environ.get("REGISTER_ACCOUNT")

### REDIS
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

### EMAIL
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
