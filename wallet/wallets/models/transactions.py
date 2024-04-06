from datetime import UTC, datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from wallets.constants import TransactionStatus
from wallets.exceptions import DateIsNotInThefuture
from wallets.models import BaseModel
from wallets.models.wallets import Wallet


class Transaction(BaseModel):
    wallet = models.ForeignKey(
        to=Wallet,
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    draw_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.uuid} - {self.amount} - {self.draw_time} - {self.status}"

    @staticmethod
    def create_transaction(
        wallet: Wallet, amount: Decimal, draw_time: datetime
    ) -> "Transaction":
        if draw_time <= datetime.now(UTC):
            raise DateIsNotInThefuture()

        transaction = Transaction(
            wallet=wallet,
            amount=amount,
            draw_time=draw_time,
            status=TransactionStatus.PENDING,
        )
        transaction.save()
        return transaction
