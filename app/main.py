from fastapi import FastAPI
from dotenv import load_dotenv
from .routes import brewery, user

app = FastAPI()

app.include_router(brewery.router)
app.include_router(user.router)

load_dotenv()
