from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.db_setup import Base
from app.api.favorites.models import Favorites


load_dotenv()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    favorites = relationship(
        "Brewery", secondary="favorites", back_populates="favorited_by"
    )
