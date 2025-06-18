from app.models.user_dto import UserDTO
from app.repositories.user_repository import UserRepository
from app.use_cases.base import BaseUseCase


class RegisterUserUseCase(BaseUseCase):

    def register_user(
            self,
            username: str,
            firstname: str,
            lastname: str,
            chat_id: int
    ):
        user = UserDTO.register_user(
            username=username,
            firstname=firstname,
            lastname=lastname,
            chat_id=chat_id
        )

        user_repo = UserRepository(self.session)
        user_repo.add_user(user)
