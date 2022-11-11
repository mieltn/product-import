from celery import Celery

import models, crud
from utils import fetchCSV
from database import SessionLocal


celery = Celery(
    "productimport",
    broker = "redis://localhost:6379/0"
)


@celery.task(bind=True)
def runImport(self, url: str):
    with SessionLocal() as db:
        data = fetchCSV(url)
        imprt = crud.getOrCreateImport(
            models.Import,
            url,
            self.request.id,
            db
        )
        imprt.task_id = self.request.id
        imprt.status = "PENDING"
        db.commit()

        for row in data:
            row['imprt_id'] = imprt.id
            crud.updateOrCreateProduct(row, db, models.Product)

        imprt.status = "SUCCESS"
        db.commit()
        return imprt.id