from pydantic import BaseModel


class Lot(BaseModel):
    node_id: int
    title: str
    price: float
    amount: int | None
