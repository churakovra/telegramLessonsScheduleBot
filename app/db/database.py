from contextlib import asynccontextmanager

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

url = URL.create(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_async_engine(url)
async_session_factory = async_sessionmaker(bind=engine, autoflush=False)


@asynccontextmanager
async def get_db():
    async with async_session_factory() as session:
        yield session
