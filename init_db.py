from app.models import Base
from db.database import engine


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()