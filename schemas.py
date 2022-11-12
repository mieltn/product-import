from pydantic import BaseModel
from datetime import datetime


class BaseImport(BaseModel):
    url: str

    class Config:
        orm_mode = True


class Import(BaseImport):
    id: int
    task_id: str
    created_on: datetime
    updated_on: datetime | None = None

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Subcategory(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Currency(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Brand(BaseModel):
    id: int
    name: str
    url: str | None = None

    class Config:
        orm_mode = True


class Color(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BaseProduct(BaseModel):
    model: str | None = None
    name: str | None = None
    current_price: float | None = None
    raw_price: float | None = None
    discount: int | None = None
    likes_count: int | None = None
    is_new: bool | None = None
    codCountry: str | None = None
    variation_0_thumbnail: str | None = None
    variation_0_image: str | None = None
    variation_1_thumbnail: str | None = None
    variation_1_image: str | None = None
    image_url: str | None = None
    url: str | None = None

    class Config:
        orm_mode = True


class InputProduct(BaseProduct):

    category: str | None = None
    subcategory: str | None = None
    currency: str | None = None
    brand: str | None = None
    brand_url: str | None = None
    variation_0_color: str | None = None
    variation_1_color: str | None = None

    class Config:
        orm_mode = True


class Product(BaseProduct):
    id: int
    model: str
    name: str
    current_price: float
    raw_price: float
    discount: int
    likes_count: int
    is_new: bool
    image_url: str
    url: str

    category: Category
    subcategory: Subcategory
    currency: Currency
    brand: Brand | None = None
    variation_0_color: Color | None = None
    variation_1_color: Color | None = None

    class Config:
        orm_mode = True


class ProductsWithDatetime(BaseModel):
    products: list[Product]
    last_import: datetime | None = None

    class Config:
        orm_mode = True
