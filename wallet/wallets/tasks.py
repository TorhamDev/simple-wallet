import json
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pydantic
from celery.utils.log import get_task_logger
from django.db import transaction

from wallet.celery import app
from wallets.constants import (
    TRANSACTION_STATUS_FAILED,
    TRANSACTION_STATUS_INPROGRESS,
    TRANSACTION_STATUS_PENDING,
    TRANSACTION_STATUS_SUCCESSFUL,
)
from wallets.models.transactions import Transaction
from wallets.utils import WithdrawFlowManager, get_redis

logger = get_task_logger(__name__)


class TransactionData(pydantic.BaseModel):
    uuid: UUID
    amount: Decimal


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


@app.task
def do_withdraw() -> None:
    r = get_redis()
    tr_to_withdraw = r.lpop("transactions", 10)

    if not tr_to_withdraw:
        logger.warning("Nothing to do!")
        return

    logger.warning(f"{tr_to_withdraw=}")
    logger.warning(f"{type(tr_to_withdraw)=}")

    with WithdrawFlowManager(tr_to_withdraw):
        with transaction.atomic():
            if tr_to_withdraw:
                to_iter = len(tr_to_withdraw)
                for _ in range(to_iter):
                    tr = tr_to_withdraw.pop().decode().replace("'", '"')
                    logger.warning(f"TR TO JSON: {tr=}, {type(tr)=}")
                    tr = TransactionData.model_validate(json.loads(str(tr)))
                    tr = (
                        Transaction.objects.select_related("wallet")
                        .select_for_update()
                        .get(uuid=tr.uuid)
                    )
                    if (tr.wallet.balance - tr.amount) < 0:
                        tr.status = TRANSACTION_STATUS_FAILED
                        tr.save()
                    else:
                        tr.wallet.decrease_balance(tr.amount)
                        tr.status = TRANSACTION_STATUS_SUCCESSFUL
                        tr.save()
