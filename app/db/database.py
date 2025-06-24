from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.config.preferences import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from app.db.orm.user import User
from app.db.orm.slot import Slot
from app.db.orm.lesson import Lesson
from app.db.orm.base import Base

url = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(url)
session_local = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(engine)
