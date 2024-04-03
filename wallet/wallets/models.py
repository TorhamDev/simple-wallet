import ulid

from django.db import models


# NOTE: maybe using ULID? idk


class Transaction(models.Model):
    ulid = models.UUIDField(default=ulid.ulid, primary_key=True)
    amount = models.BigIntegerField()
    # todo: add fields if necessary
    pass


class Wallet(models.Model):
    ulid = models.UUIDField(default=ulid.ulid, primary_key=True)
    balance = models.BigIntegerField(default=0)

    def deposit(self, amount: int):
        # todo: deposit the amount into this wallet
        pass

