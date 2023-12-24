from dotenv import load_dotenv

import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, Integer, String
from db.database import Base


load_dotenv()


class Brewery(Base):
    __tablename__ = "breweries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
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
