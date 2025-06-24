from app.enums.bot_values import UserRoles


class UserStatusException(Exception):
    def __init__(self, username: str):
        self.message = f"User {username} doesn't have access to make an operation"


class UserAddException(Exception):
    def __init__(self, username: str):
        self.message = f"Error creating user {username}: User already exists"


class UserChangeStatusException(Exception):
    def __init__(self, username: str, role: UserRoles):
        self.message = f"Can't change make {username} role {role}"


class UserNotFoundException(Exception):
    def __init__(self, username: str, role: UserRoles):
        self.message = f"{username} {role} were not found"
