from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import models, schemas, crud

import codecs
import csv
import requests

import itertools

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


def validateURL(url):
    r = requests.get(url)
    if r.status_code != status.HTTP_200_OK:
        return r, False
    return r, True


def fetchCSV(response):
    text = codecs.iterdecode(response.iter_lines(), 'utf-8')
    reader = csv.reader(text, delimiter=',')
    headers = next(reader)
    intCols = ['discount', 'likes_count', 'id']
    floatCols = ['current_price', 'raw_price']
    for line in reader:
        rowDict = {}
        for key, value in zip(headers, line):
            if value == '':
                rowDict[key] = None
            elif value == 'true':
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


@app.post("/import")
async def importProducts(request: Request, db: Session = Depends(getDB)):
    json = await request.json()

    response, urlIsValid = validateURL(json["url"])
    if not urlIsValid:
        return JSONResponse(
            {"message": "invalid url"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    data = fetchCSV(response)
    importID = crud.createImport(db, models.Import, json["url"])
    for row in data:
        row['import_id'] = importID
        pr = crud.updateOrCreateProduct(row, db, models.Product)
        if not pr:
            return JSONResponse(
                {"message": "failed to create product {}".format(row['id'])},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # break
        
    return JSONResponse(
        {"importID": importID},
        status_code = status.HTTP_201_CREATED
    )


@app.get("/import/{importID}", response_model=schemas.Import)
def getImport(importID: int, db: Session = Depends(getDB)):
    imp = crud.getImport(db, models.Import, importID)
    if not imp:
        return JSONResponse(
            {"message": "failed to get import {}".format(importID)},
            status_code = status.HTTP_404_NOT_FOUND
        )
    return imp


@app.get("/products/{productID}", response_model=schemas.Product)
def getProducts(productID, db: Session = Depends(getDB)):
    return crud.getProductByID(productID, db, models.Product)

# @app.get("/products")
# def getProducts(priceFrom: float, priceTo: float, db: Session = Depends(getDB)):
#     return crud.getProductsFromRange(priceFrom, priceTo, db, models.Product)


# @app.patch("/products/{productID}")
# def updateProduct(productID, db: Session = Depends(getDB)):


@app.delete("/products/{productID}")
def deleteProduct(productID, db: Session = Depends(getDB)):
    isDeleted = crud.deleteProduct(productID, db, models.Product)
    if not isDeleted:
        return JSONResponse(
            {"message": "failed to get product {}".format(productID)},
            status_code = status.HTTP_404_NOT_FOUND
        )

    return JSONResponse(
        {"message": "successfully deleted product {}".format(productID)},
        status_code = status.HTTP_200_OK
    )


