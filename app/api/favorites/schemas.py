from pydantic import BaseModel
from brewery.schemas import BreweryBase
from user.schemas import UserBase

class FavoriteBase(BaseModel):
    brewery: BreweryBase
    user: UserBase

class FavoriteCreate(FavoriteBase):
    pass

# Optional - If you need to update something about a favorite relationship
class FavoriteUpdate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    # You might not need an 'id' here if your Favorites table in the database 
    # is purely an association table using only user_id and brewery_id 
    id: int  

    class Config:
        orm_mode = True
