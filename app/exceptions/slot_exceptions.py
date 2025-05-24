class SlotValidationError(Exception):
    def __init__(self, message: str = "Ошибка валидации слотов"):
        super().__init__(message)

class SlotAssignError(Exception):
    def __init__(self, message: str = "Ошибка в прикреплении пользователя к слоту"):
        super().__init__(message)