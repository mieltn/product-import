from sqlalchemy.orm import Session
from sqlalchemy import update
import models
# import sys
# sys.setrecursionlimit(1500)
# from sqlalchemy.sql import text


def createOrUpdateImport(db: Session, model: models.Import, url: str):
    imp = db.query(model).filter(model.url == url).first()
    if imp:
        stmt = (
            update(model)
            .where(model.url == url)
            .values(url = url)
        )
        db.execute(stmt)
        db.refresh(imp)
    else:
        imp = model(url=url)
        db.add(imp)
        db.commit()
        db.refresh(imp)
    return imp


def getImport(db: Session, model: models.Import, importID: int):
    return db.query(model).filter(model.id == importID).first()


def getOrCreateCategory(db: Session, model: models.Category, name):
    category = db.query(model).filter(model.name == name).first()
    if category:
        return category.id
    category = model(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category.id


def getOrCreateSubcategory(db: Session, model: models.Subcategory, name: str):
    subcategory = db.query(model).filter(model.name == name).first()
    if subcategory:
        return subcategory.id
    subcategory = model(name=name)
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory.id


def getOrCreateCurrency(db: Session, model: models.Currency, name: str):
    currency = db.query(model).filter(model.name == name).first()
    if currency:
        return currency.id
    currency = model(name=name)
    db.add(currency)
    db.commit()
    db.refresh(currency)
    return currency.id


def getOrCreateBrand(db: Session, model: models.Brand, name: str, url: str = None):
    brand = db.query(model).filter(model.name == name).first()
    if not name:
        return
    if brand:
        return brand.id
    brand = model(name=name, url=url)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand.id


def getOrCreateColor(db: Session, model: models.Color, name: str):
    color = db.query(model).filter(model.name == name).first()
    if not name:
        return
    if color:
        return color.id
    color = model(name=name)
    db.add(color)
    db.commit()
    db.refresh(color)
    return color.id


def updateOrCreateProduct(
    row: dict,
    db: Session,
    model: models.Product
):
    setValues = {
        'id': row['id'],
        'model': row['model'],
        'name': row['name'],
        'current_price': row['current_price'],
        'raw_price': row['raw_price'],
        'discount': row['discount'],
        'likes_count': row['likes_count'],
        'is_new': row['is_new'],
        'codCountry': row['codCountry'],
        'variation_0_thumbnail': row['variation_0_thumbnail'],
        'variation_0_image':row['variation_0_image'],
        'variation_1_thumbnail': row['variation_1_thumbnail'],
        'variation_1_image': row['variation_1_image'],
        'image_url': row['image_url'],
        'url': row['url'],
        'category_id': getOrCreateCategory(db, models.Category, row['category']),
        'subcategory_id': getOrCreateSubcategory(db, models.Subcategory, row['subcategory']),
        'currency_id': getOrCreateCurrency(db, models.Currency, row['currency']),
        'brand_id': getOrCreateBrand(db, models.Brand, row['brand'], row['brand_url']),
        'variation_0_color_id': getOrCreateColor(db, models.Color, row['variation_0_color']),
        'variation_1_color_id': getOrCreateColor(db, models.Color, row['variation_1_color']),
        'imprt_id': row['imprt_id']
    }
    product = db.query(model).filter(model.id == row['id']).first()
    if product:
        stmt = (
            update(model)
            .where(model.id == row['id'])
            .values(**setValues)
        )
        db.execute(stmt)
        db.refresh(product)
    else:
        product = model(**setValues)
        db.add(product)
        db.commit()
        db.refresh(product)
    
    return product


def getProductByID(productID: int, db: Session, model: models.Product):
    return db.query(model).filter(model.id == productID).first()


def getProductsFromRange(priceFrom: float, priceTo: float, db: Session, model: models.Product):
    return db.query(model).filter(model.current_price > priceFrom, model.current_price < priceTo).all()


def deleteProduct(productID: int, db: Session, model: models.Product):
    rowsAffected = db.query(model).filter(model.id == productID).delete()
    if rowsAffected:
        db.commit()
        return True
    return False


