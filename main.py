from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import models, schemas, crud

from utils import validateURL, fetchCSV

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


@app.post("/import")
def importProducts(input: schemas.BaseImport, db: Session = Depends(getDB)):
    response, urlIsValid = validateURL(input.url)
    if not urlIsValid:
        return JSONResponse(
            {"message": "invalid url"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    data = fetchCSV(response)
    imprt = crud.createOrUpdateImport(db, models.Import, input.url)
    for row in data:
        row['imprt_id'] = imprt.id
        product = crud.updateOrCreateProduct(row, db, models.Product)
        if not product:
            return JSONResponse(
                {"message": "failed to create product {}".format(row['id'])},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    return JSONResponse(
        {"importID": imprt.id},
        status_code = status.HTTP_200_OK
    )


@app.get("/import/{importID}")
def getImport(importID: int, db: Session = Depends(getDB)):
    imprt = crud.getImport(db, models.Import, importID)
    if not imprt:
        return JSONResponse(
            {"message": "no import {} exists".format(importID)},
            status_code = status.HTTP_404_NOT_FOUND
        )
    return imprt


@app.get("/products/{productID}")
def getProducts(productID: int, db: Session = Depends(getDB)):
    return crud.getProductByID(productID, db, models.Product)


@app.get("/products")
def getProducts(priceFrom: float, priceTo: float, db: Session = Depends(getDB)):
    return crud.getProductsFromRange(priceFrom, priceTo, db, models.Product)


@app.patch("/products/{productID}")
def partialUpdateProduct(
    productID: int,
    setValues: schemas.ProductBase,
    db: Session = Depends(getDB)
):
    isUpdated = crud.partialUpdateProduct(productID, setValues, db, models.Product)
    if not isUpdated:
        return JSONResponse(
            {"message": "no product {} exists".format(productID)},
            status_code = status.HTTP_404_NOT_FOUND
        )
    
    return JSONResponse(
        {"message": "successfully updated product {}".format(productID)},
        status_code = status.HTTP_200_OK
    )



@app.delete("/products/{productID}")
def deleteProduct(productID: int, db: Session = Depends(getDB)):
    isDeleted = crud.deleteProduct(productID, db, models.Product)
    if not isDeleted:
        return JSONResponse(
            {"message": "no product {} exists".format(productID)},
            status_code = status.HTTP_404_NOT_FOUND
        )

    return JSONResponse(
        {"message": "successfully deleted product {}".format(productID)},
        status_code = status.HTTP_200_OK
    )


