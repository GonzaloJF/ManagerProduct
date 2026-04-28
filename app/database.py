from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

DATABASE_URL = settings.sqlalchemy_database_url()
engine = create_engine(DATABASE_URL)

sessionslocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = sessionslocal()
    try:
        yield db
    finally:
        db.close()
