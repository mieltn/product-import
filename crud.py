from sqlalchemy.orm import Session
import models

def get_or_create_category(db: Session, model: models.Category, name):
    category = db.query(model).filter(model.name == name).first()
    if category:
        return category
    else:
        category = model(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category


def get_or_create_subcategory(db: Session, model: models.Subcategory, name):
    subcategory = db.query(model).filter(model.name == name).first()
    if subcategory:
        return subcategory
    else:
        subcategory = model(name=name)
        db.add(subcategory)
        db.commit()
        db.refresh(subcategory)
        return subcategory


def get_or_create_currency(db: Session, model: models.Currency, name):
    currency = db.query(model).filter(model.name == name).first()
    if currency:
        return currency
    else:
        currency = model(name=name)
        db.add(currency)
        db.commit()
        db.refresh(currency)
        return currency


def get_or_create_brand(db: Session, model: models.Brand, name, url=None):
    brand = db.query(model).filter(model.name == name).first()
    if brand:
        return brand
    else:
        brand = model(name=name, url=url)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand


def get_or_create_color(db: Session, model: models.Color, name):
    color = db.query(model).filter(model.name == name).first()
    if color:
        return color
    else:
        color = model(name=name)
        db.add(color)
        db.commit()
        db.refresh(color)
        return color


def create_product(
    db: Session,
    data
):
    
    product = models.Product(
        model = data['model'],
        name = data['name'],
        current_price = data['current_price'],
        raw_price = data['raw_price'],
        discount = data['discount'],
        likes_count = data['likes_count'],
        is_new = data['is_new'],
        codCountry = data['codCountry'],
        variation_0_thumbnail = data['variation_0_thumbnail'],
        variation_0_image = data['variation_0_image'],
        variation_1_thumbnail = data['variation_1_thumbnail'],
        variation_1_image = data['variation_1_image'],
        image_url = data['image_url'],
        url = data['url'],
        category = get_or_create_category(db, models.Category, data['category']),
        subcategory = get_or_create_subcategory(db, models.Subcategory, data['subcategory']),
        currency = get_or_create_currency(db, models.Currency, data['currency']),
        brand = get_or_create_brand(db, models.Brand, data['brand'], data['brand_url']),
        variation_0_color = get_or_create_color(db, models.Color, data['variation_0_color']),
        variation_1_color = get_or_create_color(db, models.Color, data['variation_1_color'])
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


