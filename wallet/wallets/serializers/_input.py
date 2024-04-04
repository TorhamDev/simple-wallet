from decimal import Decimal

from django.core.validators import MinValueValidator
from rest_framework import serializers

from wallets.models import Wallet


class WalletInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("uuid", "balance")
        read_only_fields = ("uuid", "balance")


class DepositWalletInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("balance",)


class WithdrawWalletInputSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
