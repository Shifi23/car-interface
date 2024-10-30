from celery import Celery

def make_celery():
    celery = Celery('tasks', broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")
    celery.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': 'redis://localhost:6379/0',
        'default_timeout': 20
    }
    }