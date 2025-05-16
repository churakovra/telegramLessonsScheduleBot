from app.services.user_service import UserService


async def get_user_info_use_case(username: str) -> str:
    return await UserService.get_user_info(username)
