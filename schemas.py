from pydantic import BaseModel
import datetime


class BaseImport(BaseModel):
    url: str

    class Config:
        orm_mode = True


class Import(BaseImport):
    id: int
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


class ProductBase(BaseModel):
    id: int | None = None
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

    category_id: int | None = None
    subcategory_id: int | None = None
    currency_id: int | None = None
    brand_id: int | None = None
    variation_0_color_id: int | None = None
    variation_1_color_id: int | None = None
    imprt_id: int | None = None

    class Config:
        orm_mode = True


class Product(ProductBase):
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

    category_id: int
    subcategory_id: int
    currency_id: int
    imprt_id: int

    # category: Category
    # subcategory: Subcategory
    # currency: Currency
    # brand: Brand | None = None
    # variation_0_color: Color | None = None
    # variation_1_color: Color | None = None
    # imprt: Import

    class Config:
        orm_mode = True