from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from database import Base


class BaseModel(Base):
    d_create = Column(DateTime(timezone=True), server_default=func.now())
    d_change = Column(DateTime(timezone=True))


class User(BaseModel):
    __tablename__ = "user_auth"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)

    hashed_password = Column(String, nullable=False)
