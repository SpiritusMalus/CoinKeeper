from dotenv import load_dotenv
import os

load_dotenv()

MAIN_URL = os.environ.get("MAIN_URL")

### DATABASE
DATABASE_URL = os.environ.get("DATABASE_URL")

### COOKIE
LOGIN_TO_ACCOUNT = os.environ.get("LOGIN_TO_ACCOUNT")
RESET_PASS_ACCOUNT = os.environ.get("RESET_PASS_ACCOUNT")
REGISTER_ACCOUNT = os.environ.get("REGISTER_ACCOUNT")

### EMAIL
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
