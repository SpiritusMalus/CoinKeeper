from pydantic import BaseModel, EmailStr


class BaseUserModel(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str


class UserRegistration(BaseUserModel):
    email: EmailStr
    password: str
    repeat_password: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class UserLogin(BaseUserModel):
    pass
