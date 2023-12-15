from pydantic import BaseModel, Field
from typing import Optional
import uuid


class BreweryBase(BaseModel):
    name: str
    brewery_type: str
    address: str
    city: str
    state_province: str
    postal_code: str
    country: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    
    class Config:
        orm_mode=True


class BreweryRead(BreweryBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="id")


class BreweryUpdate(BaseModel):
    name: Optional[str] = None
    brewery_type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None