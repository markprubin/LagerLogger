from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import SessionLocal
from app.schemas import UserCreate, User, UserBase, UserInDB
from app.models import User as DBUser

router = APIRouter()


# Create a User
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
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

# # Update User
# @router.put('/users/{user_id', response_model=UserUpdate)


# Get a User
@router.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user.__dict__)
