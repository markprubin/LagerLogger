from fastapi import APIRouter, HTTPException
from app.services import brewery_api
from app.services.brewery_api import insert_data_into_db

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