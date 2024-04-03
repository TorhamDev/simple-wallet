from django.db import models

from wallets.models import BaseModel


class Transaction(BaseModel):
    amount = models.BigIntegerField()
    # todo: add fields if necessary
    pass
