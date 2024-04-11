from db.db_setup import Base, engine
from app.api.brewery.models import Brewery
from app.api.user.models import User
from app.api.favorites.models import Favorites


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
