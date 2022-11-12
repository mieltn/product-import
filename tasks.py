from celery import Task, shared_task
from database import getDB

import models, crud
from utils import fetchCSV


class ImportTask(Task):
    db = next(getDB())
    
    def on_success(self, retval, task_id, args, kwargs):
        (
            self.db
            .query(models.Import)
            .filter(models.Import.task_id == task_id)
            .update({"status": "SUCCESS"})
        )
        self.db.commit()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        (
            self.db
            .query(models.Import)
            .filter(models.Import.task_id == task_id)
            .update({"status": "FAILURE"})
        )
        self.db.commit()


@shared_task(base=ImportTask, bind=True)
def runImport(self, url: str):
    data = fetchCSV(url)
    imprt = crud.updateOrCreateImport(
        models.Import,
        url,
        self.request.id,
        self.db
    )

    for row in data:
        row['imprt_id'] = imprt.id
        crud.updateOrCreateProduct(row, self.db, models.Product)
