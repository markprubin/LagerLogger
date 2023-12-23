from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class User(UserBase):
    id: int


class UserInDB(UserBase):
    hashed_password: str
