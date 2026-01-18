from datetime import datetime
from pydantic import BaseModel


class BaseDTO(BaseModel):
    id: int
    created_at: datetime
    last_updated_at: datetime