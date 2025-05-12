class SlotValidationError(Exception):
    def __init__(self, message: str = "Ошибка валидации слотов"):
        super().__init__(message)