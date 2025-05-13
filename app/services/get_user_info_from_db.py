from sqlalchemy import select

from app.models.orm.user import User
from app.database import SessionLocal
from app.utils.make_user_info_response import make_user_info_response


async def get_user_info_from_db(username: str) -> str:
    user_stmt = select(User).where(User.username==username)
    with SessionLocal.begin() as session:
        user = session.scalar(user_stmt)
    if not user:
        return "Такого не нашли"
    result = make_user_info_response(user)
    return result
