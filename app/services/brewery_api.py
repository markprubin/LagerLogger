import httpx

# GET request for all breweries
async def get_all_breweries():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.openbrewerydb.org/v1/breweries')
        return response.json()