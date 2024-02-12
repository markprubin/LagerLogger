from dotenv import load_dotenv

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from db.database import Base

from app.api.favorites.models import Favorites


load_dotenv()


class Brewery(Base):
    __tablename__ = "breweries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
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
    favorited_by = relationship(
        "User", secondary="favorites", back_populates="favorites"
    )
