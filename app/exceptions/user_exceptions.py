class GetUserError(Exception):
    def __init__(self, message: str = "Ошибка в получении пользователя из бд"):
        super().__init__(message)

class UserStatusError(Exception):
    def __init__(self, message: str = "Недостаточно прав у пользователя"):
        super().__init__(message)

class AddUserError(Exception):
    def __init__(self, message: str = "Ошибка добавления пользователя. Пользователь уже существует."):
        super().__init__(message)


class ChangeUserStatusError(Exception):
    def __init__(self, message: str = "Ошибка изменения статуса пользователя."):
        super().__init__(message)