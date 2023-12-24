from db.database import engine, Base

from app.user.models import User
from app.brewery.models import Brewery


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
