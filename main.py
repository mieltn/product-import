from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import models, schemas, crud

import codecs
import csv
import requests

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/products")
# def getProducts(db: Session = Depends(getDB)):
#     products= db.query(models.Product).all()
#     return products

# @app.get("/products/{productID}")
# def getProductsByID(productID: int, db: Session = Depends(getDB)):
#     product = db.query(models.Product).get(productID)
#     return product

# @app.post("/products/new")
# def createProduct(product: schemas.Product, db: Session = Depends(getDB)):
#     newProduct = models.Product(**product.dict())
#     db.add(newProduct)
#     db.commit()
#     db.refresh(newProduct)
#     return newProduct

def fetchCSV():
    r = requests.get('https://query.data.world/s/s5gt6acvtmeahnaha2epnhlnxdiw3e')
    text = codecs.iterdecode(r.iter_lines(), 'utf-8')
    reader = csv.reader(text, delimiter=',')
    headers = next(reader)
    intCols = ['discount', 'likes_count', 'id']
    floatCols = ['current_price', 'raw_price']
    for line in reader:
        rowDict = {}
        for key, value in zip(headers, line):
            if value == 'true':
                rowDict[key] = True
            elif value == 'false':
                rowDict[key] = False
            elif key in intCols:
                rowDict[key] = int(value)
            elif key in floatCols:
                rowDict[key] = float(value)
            else:
                rowDict[key] = value
        yield rowDict

@app.get("/import")
def importProducts(db: Session = Depends(getDB)):
    data = fetchCSV()
    for row in data:
        crud.create_product(db, row)
        break

