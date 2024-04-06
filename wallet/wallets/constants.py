from django.db import models


class TransactionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESSFUL = "successful", "Successful"
    FAILED = "failed", "Failed"
    INPROGRESS = "inprogress", "Inprogress"


TRANSACTIONS_REDIS_KEY = "transactions"
