from rest_framework import serializers

from wallets.models import Wallet


class CreateWalletInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("uuid", "balance")
        read_only_fields = ("uuid", "balance")
