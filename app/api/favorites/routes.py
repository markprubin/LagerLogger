from math import fabs
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from db.db_setup import get_db
from app.utils.auth import get_current_user
from app.api.brewery.models import Brewery
from app.api.user.models import User
from app.api.favorites.schemas import FavoriteBase
from app.api.favorites.models import Favorites

router = APIRouter()


# Add Favorite
@router.post("/favorites/add", response_model=FavoriteBase)
async def add_favorite(
    brewery_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    brewery = db.query(Brewery).get(brewery_id)
    if not brewery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brewery not found"
        )

    # Check for exisiting favorite to prevent duplication
    existing_favorite = (
        db.query(Favorites)
        .filter(
            Favorites.user_id == current_user.id, Favorites.brewery_id == brewery.id
        )
        .first()
    )

    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brewery already in favorites",
        )

    # Create favorite relationship
    new_favorite = Favorites(user_id=current_user.id, brewery_id=brewery.id)
    db.add(new_favorite)

    try:
        db.commit()
        db.refresh(new_favorite)
        new_favorite.user = current_user
        new_favorite.brewery = brewery
        return new_favorite

    except Exception as e:  # General exception catching
        db.rollback()  # Consider rolling back changes
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the favorite.",
        ) from e


# Remove Favorite
@router.delete("/favorites/remove", response_model=None, status_code=status.HTTP_200_OK)
async def remove_favorite(
    brewery_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    favorite_to_remove = (
        db.query(Favorites)
        .filter(
            Favorites.user_id == current_user.id, Favorites.brewery_id == brewery_id
        )
        .first()
    )

    if not favorite_to_remove:
        raise HTTPException(status_code=404, detail="Favorite not found.")

    try:
        db.delete(favorite_to_remove)
        db.commit()
        return "Removed from favorites."

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
