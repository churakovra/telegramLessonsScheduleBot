from app.exceptions.user_exceptions import AddUserError
from app.models.user_dto import UserDTO
from app.repositories.user_repo import UserRepo


async def register_new_user_use_case(user: UserDTO):
    try:
        await UserRepo.add_user(user)
    except AddUserError:
        pass
