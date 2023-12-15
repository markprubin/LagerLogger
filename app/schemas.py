from pydantic import BaseModel
from typing import Optional

class BreweryBase(BaseModel):
    id: str
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
    
class BrewerySchema(BreweryBase):
    id: str
    
