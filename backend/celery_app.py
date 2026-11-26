from celery import Celery
celery_app = Celery(
    "parking",
    include=[
        "backend.tasks.daily_reminder",
        "backend.tasks.csv_export"
    ]
)