from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.database import get_db
from app.api.user.schemas import UserCreate, User, UserUpdate, UserPublic, UserInDB
from app.api.user.models import User as DBUser
from app.utils.auth import get_password_hash, verify_password, oauth2_scheme, get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from datetime import timedelta

router = APIRouter()


# Create a User
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = get_password_hash(user.password)
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


@router.get("/users/me")
async def read_users_me(current_user: DBUser = Depends(get_current_user)):
    return current_user


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
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if not user_db or not verify_password(form_data.password, user_db.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # create a new token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_db.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}