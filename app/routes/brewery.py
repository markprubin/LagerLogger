from email.policy import HTTP
from fastapi import APIRouter, HTTPException, status

from app.services import brewery_api
from app.services.brewery_api import insert_data_into_db
from app.schemas import BrewerySchema
from app.models import Brewery
from db.database import SessionLocal

router = APIRouter()


# Return all breweries
@router.get('/breweries')
async def get_breweries():
    return await brewery_api.get_all_breweries()

@router.post('/store_breweries')
async def store_breweries():
    try:
        data = await brewery_api.get_all_breweries()
        
        insert_data_into_db(data)
        
        return {"message": 'Data fetched and stored successfully'}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   

# Create a Brewery (POST request) 
@router.post('/create_brewery', response_model=BrewerySchema, status_code=status.HTTP_201_CREATED)
async def create_brewery(brewery: BrewerySchema):
    '''
    Return: Pydantic model object (brewery) using BrewerySchema
    '''
    
    db = SessionLocal()
    try:
        
        new_brewery = Brewery(
            **brewery.model_dump()
        )
    
        db.add(new_brewery)
        db.commit()
        db.close()
        
        return brewery
    
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=str(e))


# Update Brewery
@router.

# Delete Brewery
@router.delete('/delete_brewery/{brewery_id}', response_model=None, status_code=status.HTTP_200_OK)
async def delete_brewery(brewery_id: str):
    db = SessionLocal()
    
    try:
        brewery_to_delete = db.query(Brewery).filter(Brewery.id == brewery_id).first()
        
        if brewery_to_delete:
            db.delete(brewery_to_delete)
            db.commit()
            db.close()
            return None
        else:
            db.close()
            raise HTTPException(status_code=404, detail='Brewery not found.')
    
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=str(e))
