from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String
from db.database import Base


load_dotenv()


class Brewery(Base):
    __tablename__ = "breweries"

    id = Column(String, primary_key=True)
    name = Column(String)
    brewery_type = Column(String)
    address = Column(String)
    city = Column(String)
    state_province = Column(String)
    postal_code = Column(String)
    country = Column(String)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
