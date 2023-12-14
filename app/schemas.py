from pydantic import BaseModel
from typing import Optional

class BreweryBase(BaseModel):
    id: str
    name: str
    address: str
    city: str
    state_province: str
    postal_code: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    
class Brewery(BreweryBase):
    id: int