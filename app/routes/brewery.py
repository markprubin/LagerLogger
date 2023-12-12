from fastapi import APIRouter
from app.services import brewery_api

router = APIRouter()

@router.get("/test")
async def test_route():
    return {"message": "Test route working"}

# Return all breweries
@router.get('/breweries')
async def get_breweries():
    return await brewery_api.get_all_breweries()
