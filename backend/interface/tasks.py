from celery import shared_task
import time
from backend.interface.celery_config import celery_app


@shared_task
def test(x,y):

    time.sleep(5)
    return x / y