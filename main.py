from fastapi import FastAPI
from brewery_api import get_breweries

app = FastAPI()

# Return all breweries
@app.get('/breweries')
async def read_breweries():
    return await get_breweries()

