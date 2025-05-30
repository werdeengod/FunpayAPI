from typing import Optional
from pydantic import BaseModel


class Account(BaseModel):
    id: int
    csrf_token: str
    username: str
    balance: Optional[int] = None
