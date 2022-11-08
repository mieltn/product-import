from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    id: int
    name: str


class Subcategory(BaseModel):
    id: int
    name: str


class Currency(BaseModel):
    id: int
    name: str


class Brand(BaseModel):
    id: int
    name: str
    url: Optional[str] = None


class Color(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    id: int
    model: str
    name: str
    current_price: float
    raw_price: float
    discount: int
    likes_count: int
    is_new: bool
    codCountry: Optional[str] = None
    variation_0_thumbnail: Optional[str] = None
    variation_0_image: Optional[str] = None
    variation_1_thumbnail: Optional[str] = None
    variation_1_image: Optional[str] = None
    image_url: str
    url: str

    category: Category
    subcategory: Subcategory
    currency: Currency
    brand: Optional[Brand] = None
    variation_0_color: Optional[Color] = None
    variation_1_color: Optional[Color] = None

    class Config:
        orm_mode = True