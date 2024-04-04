from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from wallets.models import Wallet
from wallets.models.transactions import Transaction
from wallets.serializers import (
    DepositWalletInputSerializer,
    TransactionOutputSerializer,
    WalletInputSerializer,
    WalletOutputSerializer,
    WithdrawWalletInputSerializer,
)


class CreateWalletView(CreateAPIView):
    serializer_class = WalletInputSerializer

    queryset = Wallet.objects.all()


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletOutputSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"


class CreateDepositView(APIView):
    def post(self, request: Request, uuid, *args, **kwargs):
        data = DepositWalletInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        wallet = get_object_or_404(Wallet, uuid=uuid)
        wallet = wallet.deposit(data.validated_data["balance"])
        return Response(WalletOutputSerializer(instance=wallet).data)


class ScheduleWithdrawView(APIView):
    def post(self, request: Request, uuid, *args, **kwargs):
        wallet = get_object_or_404(Wallet, uuid=uuid)

        data = WithdrawWalletInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        # create the transaction
        transaction = Transaction.create_transaction(
            wallet=wallet,
            amount=data.validated_data["amount"],
            draw_time=data.validated_data["datetime"],
        )
        return Response(TransactionOutputSerializer(instance=transaction))
