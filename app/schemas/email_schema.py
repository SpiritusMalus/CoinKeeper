from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

    IMAP_USERNAME: str
    IMAP_PASSWORD: str
    IMAP_SERVER: str
    IMAP_PORT: int

    class Config:
        env_file = ".env"
