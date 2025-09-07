from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    password: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


# class User(UserBase):
#     id: int
#     is_active: bool
#     created_at: datetime

#     class Config:
#         from_attributes = True
