from db.database import engine, Base
from app.api.brewery.models import Brewery
from app.api.user.models import User


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
