from datetime import UTC, datetime
from random import randint

from celery.utils.log import get_task_logger
from django.db import transaction

from wallet.celery import app
from wallets.constants import TRANSACTION_STATUS_PENDING
from wallets.models.transactions import Transaction
from wallets.utils import get_redis

logger = get_task_logger(__name__)


@app.task
def get_transactions_to_withdraw():
    with transaction.atomic():
        transactions = (
            Transaction.objects.select_for_update()
            .filter(
                draw_time__lte=datetime.now(UTC),
                status=TRANSACTION_STATUS_PENDING,
            )
            .values("uuid", "amount")
        )
        r = get_redis()

        r.lpush("transactions", *[str(i) for i in transactions])
        logger.warning(f"{list(transactions)}")

    logger.warning(f"Executing task for user {randint(0, 999)}")
    # ... your task logic ...
    return "Task completed for user!"
