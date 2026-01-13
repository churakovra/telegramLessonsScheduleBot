from pydantic import BaseModel

from app.utils.keyboard.callback_factories.menu import MenuCallback


class ButtonDTO(BaseModel):
    text: str
    callback_data: MenuCallback
