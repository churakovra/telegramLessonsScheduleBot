class LessonsNotFoundException(Exception):
    def __init__(self):
        self.message = "Lessons were not found"


class LessonUpdateWrongSpecException(Exception):
    def __init__(self, spec):
        self.wrong_spec = spec
        self.message = f"Wrong spec {spec} for lesson update"
