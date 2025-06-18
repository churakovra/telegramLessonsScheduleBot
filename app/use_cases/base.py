from sqlalchemy.ext.asyncio import AsyncSession


class BaseUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session
