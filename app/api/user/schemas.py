from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
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


class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: Optional[str] = None
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
        from_attributes=True


class UserPublic(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    
    @classmethod
    def from_user_in_db(cls, user_in_db: UserInDB):
        return cls(**user_in_db.model_dump(exclude={"hashed_password"}))