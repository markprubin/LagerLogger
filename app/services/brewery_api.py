import httpx
import math
from app.api.brewery.models import Brewery
from db.db_setup import SessionLocal
from typing import Optional


# Get request for breweries by page
async def get_breweries_pagination(page: Optional[int] = 1):
    url = "https://api.openbrewerydb.org/v1/breweries"
    per_page = (
        200  # You can adjust this number based on how many results you want per page
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"per_page": per_page, "page": page})
        data = response.json()

    return data


# GET request for all breweries (API CALL - DO NOT USE - WILL OVERLOAD API)
# async def get_all_breweries():
#     url = "https://api.openbrewerydb.org/v1/breweries"
#     meta_url = "https://api.openbrewerydb.org/v1/breweries/meta"
#     async with httpx.AsyncClient() as client:
#         meta_response = await client.get(meta_url)
#         meta_data = meta_response.json()
#
#         total_results = int(meta_data.get("total", 0))
#         per_page = 200
#         total_pages = math.ceil(total_results / per_page)
#
#         all_results = []
#
#         # Fetch all pages
#         for page in range(1, total_pages):
#             response = await client.get(
#                 url, params={"per_page": per_page, "page": page}
#             )
#             data = response.json()
#
#             all_results.extend(data)
#
#     return all_results


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
