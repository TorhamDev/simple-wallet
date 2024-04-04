from random import randint

from celery.utils.log import get_task_logger

from wallet.celery import app

logger = get_task_logger(__name__)


@app.task()
def withdraw_task():
    # Perform your task logic here using the provided arguments
    # This task will be executed in the background by a Celery worker after the delay
    logger.warning(f"Executing task for user {randint(0, 999)}")
    # ... your task logic ...
    return "Task completed for user!"
