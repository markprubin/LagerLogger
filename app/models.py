from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import Column, Integer, String
from db.database import Base

class Brewery(Base):
    __tablename__ = "breweries"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    state_province = Column(String)
    postal_code = Column(String)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website_url = Column(String, nullable=True)

