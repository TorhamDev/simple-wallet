from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F

from wallets.models import BaseModel


class Wallet(BaseModel):
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
    )

    def deposit(self, amount: Decimal) -> "Wallet":
        # NOTE: we are doing incremental update instead of row lock update
        # why? bc is better for this type of updates
        wallet = Wallet.objects.get(pk=self.pk)
        wallet.balance = F("balance") + amount
        wallet.save()
        wallet.refresh_from_db()
        return wallet

    def decrease_balance(self, amount: Decimal) -> "Wallet":
        # NOTE: we are doing incremental update instead of row lock update
        # why? bc is better for this type of updates
        wallet = Wallet.objects.get(pk=self.pk)
        wallet.balance = F("balance") - amount
        wallet.save()
        wallet.refresh_from_db()
        return wallet
