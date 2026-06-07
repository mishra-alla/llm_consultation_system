from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "bot_service",
    broker=settings.rabbitmq_url,
    backend="rpc://",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Импортируем задачи
celery_app.autodiscover_tasks(['app.tasks'], force=True)

@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
