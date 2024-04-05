from datetime import UTC, datetime

from celery.utils.log import get_task_logger
from django.db import transaction

from wallet.celery import app
from wallets.constants import TRANSACTION_STATUS_INPROGRESS, TRANSACTION_STATUS_PENDING
from wallets.models.transactions import Transaction
from wallets.utils import get_redis

logger = get_task_logger(__name__)


@app.task
def get_transactions_to_withdraw() -> None:
    with transaction.atomic():
        transactions = Transaction.objects.select_for_update().filter(
            draw_time__lte=datetime.now(UTC),
            status=TRANSACTION_STATUS_PENDING,
        )

        if transactions:
            tr_to_redis = []
            for tr in transactions.values("uuid", "amount"):
                tr["uuid"] = str(tr["uuid"])
                tr_to_redis.append(str(tr))
            r = get_redis()

            r.lpush("transactions", *tr_to_redis)

            for tr in transactions:
                tr.status = TRANSACTION_STATUS_INPROGRESS

            Transaction.objects.bulk_update(transactions, ["status"])
