from pydantic import BaseModel

class Product(BaseModel):
    name: str
    model: str
    current_price: float