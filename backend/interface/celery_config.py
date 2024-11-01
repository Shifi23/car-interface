from celery.app import Celery

celery_app = Celery(__name__, broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    broker_pool_limit=None,
    broker_heartbeat=10,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=None,
)

celery_app.autodiscover_tasks(
    [
        "backend.interface.controls.tasks",
        "backend.interface.tasks"

    ]
)