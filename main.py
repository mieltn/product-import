from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def getProducts(db: Session = Depends(getDB)):
    products= db.query(models.Product).all()
    return products

@app.get("/products/{productID}")
def getProductsByID(productID: int, db: Session = Depends(getDB)):
    product = db.query(models.Product).get(productID)
    return product

@app.post("/products/new")
def createProduct(product: schemas.Product, db: Session = Depends(getDB)):
    newProduct = models.Product(**product.dict())
    db.add(newProduct)
    db.commit()
    db.refresh(newProduct)
    return newProduct
