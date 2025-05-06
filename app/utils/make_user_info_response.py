from app.models.user import User


def make_user_info_response(user: User) -> str:
    role = ""
    match user:
        case _ if user.teacher:
            role = "Преподаватель"
        case _ if user.student:
            role = "Студент"
        case _ if user.admin:
            role = "Администратор"
    return f"""
        Пользователь {user.username}
        Дата регистрации {user.dt_reg}
        Роль {role}
    """
