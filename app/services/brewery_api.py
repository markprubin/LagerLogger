import httpx
from app.api.brewery.models import Brewery
from db.database import SessionLocal
from geopy.geocoders import Nominatim


# GET request for all breweries
async def get_all_breweries():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.openbrewerydb.org/v1/breweries")
        return response.json()


# Fetch and Insert Function
def insert_data_into_db(data):
    # Create a new DB session
    db = SessionLocal()
    try:
        for item in data:
            # Create instance of model with the data
            brewery = Brewery(
                id=item.get("id"),
                name=item.get("name"),
                brewery_type=item.get("brewery_type"),
                address=item.get("address_1"),
                city=item.get("city"),
                state_province=item.get("state_province"),
                postal_code=item.get("postal_code"),
                country=item.get("country"),
                latitude=item.get("latitude"),
                longitude=item.get("longitude"),
                phone=item.get("phone"),
                website_url=item.get("website_url"),
            )
            # Add new record to session
            db.add(brewery)

        # Commit session to save records
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()  # Rollback in case of error
    finally:
        db.close()  # Close session


def get_coordinates(address, city, state_province, postal_code):
    """
    Fetches latitude and longitude from geocoding API
    Args:
        address(str): Street address
        city(str): City name
        state_province(str): State or Province name
        postal_code (str): Postal code
    Returns:
        tuple: (latitude, longitude) if found, otherwise None
    """
    geolocator = Nominatim(user_agent="beergeocoder")
    location = geolocator.geocode(f"{address}, {city}, {state_province}, {postal_code}")
    if location:
        return location.latitude, location.longitude
    else:
        return None
    
