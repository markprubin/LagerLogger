from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
import traceback
import logging

from app.services import brewery_api
from app.services.brewery_api import insert_data_into_db, get_coordinates
from app.api.brewery.schemas import BreweryCreate, BreweryUpdate, BreweryBase
from app.api.brewery.models import Brewery
from db.database import get_db

router = APIRouter()

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.ERROR)


# Return all breweries
@router.get("/breweries")
async def get_breweries():
    return await brewery_api.get_all_breweries()


@router.get("/breweries/{brewery_id}", response_model=BreweryBase)
async def get_brewery(brewery_id: str, db: Session = Depends(get_db)):
    try:
        brewery_db = db.query(Brewery).filter(Brewery.id == brewery_id).first()
        if brewery_db is None:
            raise HTTPException(status_code=404, detail="Brewery not found.")
        brewery_in_db = BreweryBase.from_orm(brewery_db)
        return brewery_in_db
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/store_breweries")
async def store_breweries():
    try:
        data = await brewery_api.get_all_breweries()

        insert_data_into_db(data)

        return {"message": "Data fetched and stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create a Brewery (POST request)
@router.post(
    "/create_brewery", response_model=BreweryCreate, status_code=status.HTTP_201_CREATED
)
async def create_brewery(brewery: BreweryCreate, db: Session = Depends(get_db)):
    """
    Return: Pydantic model object (brewery) using BrewerySchema
    """

    try:
        new_brewery = Brewery(**brewery.model_dump())
        db.add(new_brewery)
        db.commit()
        return brewery

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Update Brewery
@router.put("/breweries/{brewery_id}", response_model=BreweryUpdate)
async def update_brewery(
    brewery_id: str, brewery_update: BreweryUpdate, db: Session = Depends(get_db)
):
    try:
        existing_brewery = db.query(Brewery).filter(Brewery.id == brewery_id).first()
        if existing_brewery:
            for key, value in brewery_update.model_dump(exclude_unset=True).items():
                setattr(existing_brewery, key, value)
            db.commit()
            db.refresh(existing_brewery)
            return existing_brewery
        else:
            raise HTTPException(status_code=404, detail="Brewery not found.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Delete Brewery
@router.delete(
    "/delete_brewery/{brewery_id}", response_model=None, status_code=status.HTTP_200_OK
)
async def delete_brewery(brewery_id: str, db: Session = Depends(get_db)):
    try:
        brewery_to_delete = db.query(Brewery).filter(Brewery.id == brewery_id).first()

        if brewery_to_delete:
            db.delete(brewery_to_delete)
            db.commit()
            return None
        else:
            raise HTTPException(status_code=404, detail="Brewery not found.")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
