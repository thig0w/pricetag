# -*- coding: utf-8 -*-
import os

from celery import Celery, shared_task
from celery.schedules import crontab


class Config:
    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )

    CELERY_BEAT_SCHEDULE: dict = {
        "send_credit_report": {
            "task": "credit_report",
            "schedule": 10,
            #'options': {'queue' : 'periodic'},
        },
    }
    CELERY_TIMEZONE: str = "America/Sao_Paulo"


settings = Config()

celery_app = Celery()
celery_app.config_from_object(settings, namespace="CELERY")
celery_app.conf.beat_schedule = {
    # Executes every 3 hours
    "find-prices-3h": {
        "task": "credit_report",
        "schedule": crontab(hour="*/3", minute="0"),
    },
}


@shared_task()
def add(a, b):
    for i in range(a, b):
        print(i)
    return {"number": a + b}


@shared_task(name="credit_report")
def force_add():
    add.delay(2, 2)
