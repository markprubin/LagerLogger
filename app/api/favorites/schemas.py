from pydantic import BaseModel
from app.api.brewery.schemas import BreweryBase
from app.api.user.schemas import UserBase

class FavoriteBase(BaseModel):
    brewery: BreweryBase
    user: UserBase

class FavoriteCreate(FavoriteBase):
    pass

# To update something about a favorite relationship
class FavoriteUpdate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    # Just in case if deciding to switch to creating an favorite_id
    id: int  

    class Config:
        orm_mode = True
