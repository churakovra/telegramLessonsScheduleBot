class LessonsNotFoundException(Exception):
    def __init__(self):
        self.message = "Lessons were not found"
