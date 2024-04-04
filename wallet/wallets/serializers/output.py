from rest_framework import serializers

from wallets.models import Transaction, Wallet


class WalletOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
