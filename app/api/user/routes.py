from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from app.api.user.schemas import UserCreate, User, UserUpdate, UserPublic, UserInDB, UserLogin
from app.api.user.models import User as DBUser
from app.utils.auth import hash_password, verify_password

router = APIRouter()


# Create a User
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(user.password)
        new_user = DBUser(
            username=user.username,
            email=user.email,
            password=hashed_password,
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

        if user_to_update is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.first_name is not None:
            user_to_update.first_name = user.first_name
        if user.last_name is not None:
            user_to_update.last_name = user.last_name
        if user.email is not None:
            user_to_update.email = user.email
        db.add(user_to_update)
        db.commit()
        return user_to_update

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Get a User
@router.get("/users/{user_id}", response_model=UserPublic)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_db = db.query(DBUser).filter(DBUser.id == user_id).first()
        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_in_db = UserInDB.from_orm(user_db)
        print(user_in_db)
        user_response = UserPublic.from_user_in_db(user_in_db)
        return user_response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Delete a User
@router.delete(
    "/delete_user/{user_id}", response_model=None, status_code=status.HTTP_200_OK
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


# Authenticate User

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(DBUser).filter(DBUser.username == user.username).first()
    if user_db and verify_password(user.password, user_db.password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Login failed")
