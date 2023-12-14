import httpx
from app.models import Brewery
from db.database import SessionLocal

# GET request for all breweries
async def get_all_breweries():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.openbrewerydb.org/v1/breweries')
        return response.json()

# Fetch and Insert Function
def insert_data_into_db(data):
    # Create a new DB session
    db = SessionLocal()
    try:
        for item in data:
            # Create instance of model with the data
            brewery = Brewery(
                id=item.get('id'),
                name=item.get('name'),
                address=item.get('address'),
                city=item.get('city'),
                state_province=item.get('state_province'),
                postal_code=item.get('postal_code'),
                latitude=item.get('latitude'),
                longitude=item.get('longitude'),
                phone=item.get('phone'),
                website_url=item.get('website_url')
            )
            # Add new record to session
            db.add(brewery)
            
        # Commit session to save records
        db.commit()
    except Exception as e:
        print(f'Error: {e}')
        db.rollback() # Rollback in case of error
    finally:
        db.close() # Close session