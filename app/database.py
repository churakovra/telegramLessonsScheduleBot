from contextlib import asynccontextmanager

from sqlalchemy import URL, create_engine, false
from sqlalchemy.orm import sessionmaker

from config.preferences import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

url = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

