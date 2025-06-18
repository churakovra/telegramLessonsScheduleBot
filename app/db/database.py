from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.preferences import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

url = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_async_engine(url)
async_session = async_sessionmaker(bind=engine, autoflush=False)
