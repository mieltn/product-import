from pydantic import BaseModel
import datetime


class Import(BaseModel):
    id: int
    url: str
    created_on: datetime.datetime
    updated_on: datetime.datetime | None = None

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


class Product(BaseModel):
    id: int
    model: str
    name: str
    current_price: float
    raw_price: float
    discount: int
    likes_count: int
    is_new: bool
    codCountry: str | None = None
    variation_0_thumbnail: str | None = None
    variation_0_image: str | None = None
    variation_1_thumbnail: str | None = None
    variation_1_image: str | None = None
    image_url: str
    url: str

    category: Category
    subcategory: Subcategory
    currency: Currency
    brand: Brand | None = None
    variation_0_color: Color | None = None
    variation_1_color: Color | None = None

    import_id: int

    class Config:
        orm_mode = True