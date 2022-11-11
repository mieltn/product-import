from sqlalchemy.orm import Session
from sqlalchemy import update
import models


def getOrCreateImport(model: models.Import, url: str, taskID: str, db: Session):
    imprt = db.query(model).filter(model.url == url).first()
    if imprt:
        return imprt
    imprt = model(url=url, task_id=taskID)
    db.add(imprt)
    db.commit()
    db.refresh(imprt)
    return imprt


def getImport(db: Session, model: models.Import, taskID: str):
    return db.query(model).filter(model.task_id == taskID).first()


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
    row['category'] = getOrCreateCategory(
        db, models.Category, row.pop('category', None)
    )
    row['subcategory_id'] = getOrCreateSubcategory(
        db, models.Subcategory, row.pop('subcategory', None)
    )
    row['currency_id'] = getOrCreateCurrency(
        db, models.Currency, row.pop('currency', None)
    )
    row['brand_id'] = getOrCreateBrand(
        db, models.Brand, row.pop('brand', None), row.pop('brand_url', None)
    )
    row['variation_0_color_id'] = getOrCreateColor(
        db, models.Color, row.pop('variation_0_color', None)
    )
    row['variation_1_color_id'] = getOrCreateColor(
        db, models.Color, row.pop('variation_1_color', None)
    )

    product = db.query(model).filter(model.id == row['id']).first()
    if product:
        stmt = (
            update(model)
            .where(model.id == row['id'])
            .values(**row)
        )
        db.execute(stmt)
        db.refresh(product)
    else:
        product = model(**row)
        db.add(product)
        db.commit()
        db.refresh(product)
        
    return product


def getProductByID(productID: int, db: Session, model: models.Product):
    return db.query(model).filter(model.id == productID).first()


def getProductsFromRange(priceFrom: float, priceTo: float, db: Session, model: models.Product):
    return db.query(model).filter(model.current_price > priceFrom, model.current_price < priceTo).all()


def partialUpdateProduct(productID: int, row: dict, db: Session, model: models.Product):

    if 'category' in row:
        row['category_id'] = getOrCreateCategory(
            db, models.Category, row.pop('category', None)
        )
    if 'subcategory' in row:
        row['subcategory_id'] = getOrCreateSubcategory(
            db, models.Subcategory, row.pop('subcategory', None)
        )
    if 'currency' in row:
        row['currency_id'] = getOrCreateCurrency(
            db, models.Currency, row.pop('currency', None)
        )
    if 'brand' in row:
        row['brand_id'] = getOrCreateBrand(
            db, models.Brand, row.pop('brand', None), row.pop('brand_url', None)
        )
    if 'variation_0_color' in row:
        row['variation_0_color_id'] = getOrCreateColor(
            db, models.Color, row.pop('variation_0_color', None)
        )
    if 'variation_1_color' in row:
        row['variation_1_color_id'] = getOrCreateColor(
            db, models.Color, row.pop('variation_1_color', None)
        )

    rowsAffected = db.query(model).filter(model.id == productID).update(row)
    if rowsAffected:
        db.commit()
        return True
    return False


def deleteProduct(productID: int, db: Session, model: models.Product):
    rowsAffected = db.query(model).filter(model.id == productID).delete()
    if rowsAffected:
        db.commit()
        return True
    return False


