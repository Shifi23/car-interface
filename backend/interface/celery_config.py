from celery.app import Celery

celery_app = Celery(__name__, broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")


celery_app.autodiscover_tasks(
    [
        "backend.interface.controls.tasks",
        "backend.interface.tasks"

    ]
)