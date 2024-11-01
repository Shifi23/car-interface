from celery import shared_task
import time

from celery.app import Celery

celery_app = Celery(__name__, broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")

@shared_task
def test(x,y):

    time.sleep(5)
    return x / y