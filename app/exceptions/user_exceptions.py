from app.enums.bot_values import UserRoles


class UserStatusException(Exception):
    def __init__(self, username: str):
        self.message = f"User {username} doesn't have access to make an operation"


class UserAddException(Exception):
    def __init__(self, username: str):
        self.message = f"Error creating user {username}: User already exists"


class UserChangeStatusException(Exception):
    def __init__(self, username: str, role: UserRoles, initiator_username: str):
        self.message = (
            f"Can't change {username} role {role}. "
            f"Initiator {initiator_username} has not enough rights do make this operation"
        )


class UserNotFoundException(Exception):
    def __init__(self, username: str, role: UserRoles):
        self.message = f"{username} {role} were not found"
