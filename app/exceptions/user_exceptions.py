from app.enums.bot_values import UserRoles


class UserRoleException(Exception):
    def __init__(self, username: str):
        self.message = f"User {username} doesn't have access to make an operation"


class UserAddException(Exception):
    def __init__(self, username: str):
        self.message = f"Error creating user {username}: User already exists"


class UserChangeRoleException(Exception):
    def __init__(self, username: str, role: UserRoles, initiator_username: str):
        self.message = (
            f"Can't change {username} role {role}. "
            f"Initiator {initiator_username} has not enough rights do make this operation"
        )


class UserNotFoundException(Exception):
    def __init__(self, username: str, role: UserRoles | None):
        self.message = f"{username} {role} were not found"


class UserUnknownRoleException(Exception):
    def __init__(self, username: str | None, role: UserRoles | None):
        if username:
            self.message = f"{username} has unknown role {role}"
        elif role:
            self.message = f"Unknown role {role}"
