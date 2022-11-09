from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Import(Base):
    __tablename__ = "imports"
    id = Column(Integer, primary_key=True)
    url = Column(String(256))
    created_on = Column(DateTime, default=datetime.datetime.now)
    updated_on = Column(DateTime, onupdate=datetime.datetime.now)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class Subcategory(Base):
    __tablename__ = "subcategories"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    url = Column(String(128), nullable=True)


class Color(Base):
    __tablename__ = "colors"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    model = Column(String(128))
    name = Column(String(256))
    current_price = Column(Float(precision=2))
    raw_price = Column(Float(precision=2))
    discount = Column(Integer)
    likes_count = Column(Integer)
    is_new = Column(Boolean)
    codCountry = Column(String(128), nullable=True)
    variation_0_thumbnail = Column(String(256), nullable=True)
    variation_0_image = Column(String(256), nullable=True)
    variation_1_thumbnail = Column(String(256), nullable=True)
    variation_1_image = Column(String(256), nullable=True)
    image_url = Column(String(256))
    url = Column(String(256))

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")

    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    subcategory = relationship("Subcategory")

    currency_id = Column(Integer, ForeignKey("currencies.id"))
    currency = relationship("Currency")

    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    brand = relationship("Brand")

    variation_0_color_id = Column(Integer, ForeignKey("colors.id"), nullable=True)
    variation_0_color = relationship("Color", foreign_keys='Product.variation_0_color_id')
    
    variation_1_color_id = Column(Integer, ForeignKey("colors.id"), nullable=True)
    variation_1_color = relationship("Color", foreign_keys='Product.variation_1_color_id')

    import_id = Column(Integer, ForeignKey("colors.id"))







