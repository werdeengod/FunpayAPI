from pydantic import BaseModel


class Review(BaseModel):
    username: str
    order_code: str
    date: str
    text: str
