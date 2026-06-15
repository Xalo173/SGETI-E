from celery import Celery

from app.core.config import settings

celery_app = Celery("auditai", broker=settings.redis_url, backend=settings.redis_url, include=["app.tasks.report_tasks"])
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "reindex-knowledge-weekly": {
            "task": "app.tasks.report_tasks.reindex_knowledge_task",
            "schedule": 60 * 60 * 24 * 7,
        }
    },
)
