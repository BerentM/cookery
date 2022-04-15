from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = 'sqlite:///cookery/data/database.db'
POSTGRESQL_DATABASE_URL = f"postgresql+psycopg2://{os.environ['postgres_user']}:{os.environ['postgres_password']}@apiberentm.hopto.org/cookery"

engine = create_engine(
    POSTGRESQL_DATABASE_URL,
    # connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
