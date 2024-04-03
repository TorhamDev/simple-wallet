from rest_framework import serializers

from wallets.models import Wallet


class WalletOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
