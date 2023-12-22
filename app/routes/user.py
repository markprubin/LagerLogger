from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from app.schemas import UserCreate, User, UserBase, UserInDB
from app.models import User

router = APIRouter()


# Create a User
@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    db = SessionLocal()

    try:
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.close()
        return user

    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=str(e))
