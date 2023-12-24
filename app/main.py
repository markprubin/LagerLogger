from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.brewery.routes import router as brewery_router
from app.api.user.routes import router as user_router

app = FastAPI()

# Include routers from the 'api' directory
app.include_router(brewery_router, tags=["Brewery"])
app.include_router(user_router, tags=["User"])

# Load environment variables
load_dotenv()
