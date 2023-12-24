from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from app.api.user.schemas import UserCreate, User, UserUpdate
from app.api.user.models import User as DBUser

router = APIRouter()


# Create a User
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = DBUser(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        db.add(new_user)
        db.commit()
        return new_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Update User
@router.put("/users/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        user_to_update = db.query(DBUser).filter(DBUser.id == user_id).first()
        if user_to_update is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_to_update.first_name = user.first_name
        user_to_update.last_name = user.last_name
        user_to_update.email = user.email
        db.add(user_to_update)
        db.commit()
        return user_to_update

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Get a User
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Delete a User
@router.delete(
    "delete_user/{user_id", response_model=None, status_code=status.HTTP_200_OK
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_to_delete = db.query(DBUser).filter(DBUser.id == user_id).first()
        if user_to_delete:
            db.delete(user_to_delete)
            db.commit()
            return None
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
