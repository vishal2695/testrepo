from celery import shared_task
import time

@shared_task
def test_task(name):
    time.sleep(5)
    return f"Hello {name}, task completed!"