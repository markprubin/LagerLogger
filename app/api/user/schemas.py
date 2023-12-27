from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int


class UserInDB(UserBase):
    hashed_password: str
