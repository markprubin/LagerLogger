from db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import ForeignKey


class Favorites(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    brewery_id = Column(String, ForeignKey("breweries.id"), primary_key=True)
