from pydantic import BaseModel

from app.utils.keyboards.callback_factories.menu import BaseMenu


class ButtonDTO(BaseModel):
    text: str
    callback_data: BaseMenu
