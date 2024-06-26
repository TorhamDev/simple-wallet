import json
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pydantic
from celery.utils.log import get_task_logger
from django.db import transaction

from wallet.celery import app
from wallets.constants import TRANSACTIONS_REDIS_KEY, TransactionStatus

# better to use `import exceptions` if there is more than one thing to import
from wallets.models.transactions import Transaction
from wallets.utils import WithdrawHandler, get_redis, handle_third_party

logger = get_task_logger(__name__)


class TransactionData(pydantic.BaseModel):
    uuid: UUID
    amount: Decimal


@app.task
def get_transactions_to_withdraw() -> None:
    with transaction.atomic():
        transactions = Transaction.objects.select_for_update().filter(
            draw_time__lte=datetime.now(UTC),
            status=TransactionStatus.PENDING,
        )

        if transactions:
            logger.debug(f"get_transactions_to_withdraw: {transactions=}")
            tr_to_redis = []
            for tr in transactions.values("uuid", "amount"):
                tr["uuid"] = str(tr["uuid"])
                tr["amount"] = float(tr["amount"])
                tr_to_redis.append(str(tr))
            r = get_redis()

            r.lpush(TRANSACTIONS_REDIS_KEY, *tr_to_redis)

            for tr in transactions:
                tr.status = TransactionStatus.INPROGRESS
            logger.debug(
                f"updating transactions status to {TransactionStatus.INPROGRESS} for {tr_to_redis}"
            )

            Transaction.objects.bulk_update(transactions, ["status"])


@app.task
def do_withdraw() -> None:
    r = get_redis()
    tr_to_withdraw = r.lpop(TRANSACTIONS_REDIS_KEY, 10)

    if not tr_to_withdraw:
        logger.debug("Nothing to do!")
        return

    logger.debug(f"Start do_wthidraw with: {tr_to_withdraw=}")

    to_iter = len(tr_to_withdraw)
    for _ in range(to_iter):
        pure_tr = tr_to_withdraw.pop()
        with WithdrawHandler(pure_tr):
            tr = pure_tr.decode().replace("'", '"')
            tr = TransactionData.model_validate(json.loads(str(tr)))
            with transaction.atomic():
                logger.debug(f"Start SQL transaction for : {pure_tr=}")
                tr = (
                    Transaction.objects.select_related("wallet")
                    .select_for_update()
                    .get(uuid=tr.uuid)
                )
                if (tr.wallet.balance - tr.amount) < 0:
                    tr.status = TransactionStatus.FAILED
                    tr.save(update_fields=["status"])
                    logger.debug(f"withdraw fail bc of low balance for : {pure_tr=}")
                else:
                    logger.debug(f"Ourside withdraw successed for : {pure_tr=}")
                    tr.wallet.decrease_balance(tr.amount)
                    tr.status = TransactionStatus.SUCCESSFUL
                    tr.save(update_fields=["status"])

                logger.debug(f"Requesting 3rd party for : {pure_tr=}")
                handle_third_party()
