from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.brewery import router

app = FastAPI()

app.include_router(router)

load_dotenv()
