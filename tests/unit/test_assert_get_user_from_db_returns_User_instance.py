from app.models.orm.user import User
from app.services.get_user_from_db import get_user


async def test_assert_get_user_from_db_returns_User_instance():
    user = await get_user("johndoe")
    assert isinstance(user, User) == True