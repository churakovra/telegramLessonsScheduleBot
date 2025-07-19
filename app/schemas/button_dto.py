from pydantic import BaseModel

from app.utils.keyboards.callback_factories.base import BaseMenuCallback


class ButtonDTO(BaseModel):
    text: str
    callback_data: BaseMenuCallback
