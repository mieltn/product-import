from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import create_app
import models, schemas, crud, tasks
from database import getDB
from utils import validateURL

from celery.result import AsyncResult


app = create_app()
celery = app.celery_app


@app.post("/import")
def importProducts(input: schemas.BaseImport):

    urlIsValid = validateURL(input.url)
    if not urlIsValid:
        return JSONResponse(
            {"message": "invalid url"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    tsk = tasks.runImport.delay(input.url)

    return JSONResponse(
        {"message": "successfully started the import", "taskID": tsk.id},
        status_code = status.HTTP_200_OK
    )
    

@app.get("/import/{taskID}")
def getImport(taskID: str, db: Session = Depends(getDB)):
    imprt = crud.getImport(db, models.Import, taskID)
    if not imprt:
        return JSONResponse(
            {"message": "no import with task id {} exists".format(taskID)},
            status_code = status.HTTP_404_NOT_FOUND
        )
    
    result = AsyncResult(taskID)
    return JSONResponse(
        {
            "taskID": result.id,
            "status": result.status
        },
        status_code = status.HTTP_200_OK
    )


@app.get("/product", response_model=schemas.ProductsWithDatetime)
def getProducts(priceFrom: float, priceTo: float, db: Session = Depends(getDB)):
    products = crud.getProductsFromRange(priceFrom, priceTo, db, models.Product)
    imprt = crud.getLastImport(db, models.Import)
    response = schemas.ProductsWithDatetime(products=products, last_import=imprt.updated_on)
    return response


@app.patch("/product/{productID}")
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


@app.delete("/product/{productID}")
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

