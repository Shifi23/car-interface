from celery import shared_task
import time

@shared_task(base=QueueOnce)
def test(x,y):

    time.sleep(5)
    return x / y