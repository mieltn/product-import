from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal

import models, schemas, crud
from utils import validateURL, fetchCSV


app = FastAPI()

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
        break
        
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


@app.get("/products/{productID}", response_model=schemas.Product)
def getProducts(productID: int, db: Session = Depends(getDB)):
    return crud.getProductByID(productID, db, models.Product)


@app.get("/products")
def getProducts(priceFrom: float, priceTo: float, db: Session = Depends(getDB)):
    return crud.getProductsFromRange(priceFrom, priceTo, db, models.Product)


@app.patch("/products/{productID}", response_model=schemas.Product)
def partialUpdateProduct(
    productID: int,
    setValues: schemas.InputProduct,
    db: Session = Depends(getDB)
):
    row = setValues.dict(exclude_unset=True)
    row['id'] = productID
    isUpdated = crud.partialUpdateProduct(productID, row, db, models.Product)

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


