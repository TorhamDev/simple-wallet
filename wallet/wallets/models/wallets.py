from django.db import models

from wallets.models import BaseModel


class Wallet(BaseModel):
    balance = models.BigIntegerField(default=0)

    def deposit(self, amount: int):
        # todo: deposit the amount into this wallet
        pass
