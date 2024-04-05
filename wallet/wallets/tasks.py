import json
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pydantic
from celery.utils.log import get_task_logger
from django.db import transaction
from redis.exceptions import ConnectionError, RedisError

from wallet.celery import app
from wallets.constants import (
    TRANSACTION_STATUS_FAILED,
    TRANSACTION_STATUS_INPROGRESS,
    TRANSACTION_STATUS_PENDING,
    TRANSACTION_STATUS_SUCCESSFUL,
)
from wallets.models.transactions import Transaction
from wallets.utils import get_redis, request_third_party_deposit

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
    logger.warning(f"{tr_to_withdraw=}")

    if tr_to_withdraw:
        logger.warning("TRDY")
        for tr in tr_to_withdraw:
            try:
                logger.warning(f"{tr=}")
                tr = TransactionData(**json.load(tr))

                # request to 3rd party
                result_3rd = request_third_party_deposit()
                logger.warning(f"3RD RESULT: {result_3rd}")
                if result_3rd:
                    with transaction.atomic():
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

            except json.decoder.JSONDecodeError as e:
                # do log
                logger.warning(f"JSON ERROR: {e}")
                ...
            except pydantic.ValidationError:
                # do log
                print("PY ERROR")
                ...
            except (RedisError, ConnectionError):
                # push back to the redis
                ...
