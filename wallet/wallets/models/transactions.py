from datetime import datetime
from decimal import Decimal

from django.db import models

from wallets.constants import TRANSACTION_STATUS, TRANSACTION_STATUS_PENDING
from wallets.models import BaseModel
from wallets.models.wallets import Wallet


class Transaction(BaseModel):
    wallet = models.ForeignKey(
        to=Wallet,
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.BigIntegerField()
    draw_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUS,
        blank=True,
        null=True,
    )

    @staticmethod
    def create_transaction(
        wallet: Wallet, amount: Decimal, draw_time: datetime
    ) -> "Transaction":
        transaction = Transaction(
            wallet=wallet,
            amount=amount,
            draw_time=draw_time,
            status=TRANSACTION_STATUS_PENDING,
        )
        transaction.save()
        return transaction
