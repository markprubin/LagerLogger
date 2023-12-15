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
    db = SessionLocal()
    new_brewery = Brewery(
        id = brewery.id,
        name = brewery.name,
        brewery_type = brewery.brewery_type,
        address = brewery.address,
        city = brewery.city,
        state_province = brewery.state_province,
        postal_code = brewery.postal_code,
        country = brewery.country,
        latitude = brewery.latitude,
        longitude = brewery.longitude,
        phone = brewery.phone,
        website_url = brewery.website_url
    )
    
    db.add(new_brewery)
    db.commit()
    
    return new_brewery
