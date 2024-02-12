from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.brewery.routes import router as brewery_router
from app.api.user.routes import router as user_router
from app.api.favorites.routes import router as favorites_router

app = FastAPI()

# Include routers from the 'api' directory
app.include_router(brewery_router, tags=["Brewery"])
app.include_router(user_router, tags=["User"])
app.include_router(favorites_router, tags=["Favorites"])

# Load environment variables
load_dotenv()
