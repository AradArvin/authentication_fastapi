from pydantic import BaseModel, EmailStr, ValidationError
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
    role: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    role: str
    join_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


class UserTokenResponse(BaseModel):
    access: str | None = None
    refresh: str | None = None


class UserLogOut(BaseModel):
    user_id: str