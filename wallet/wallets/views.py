from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from wallets.models import Wallet
from wallets.serializers import (
    DepositWalletInputSerializer,
    WalletInputSerializer,
    WalletOutputSerializer,
)


class CreateWalletView(CreateAPIView):
    serializer_class = WalletInputSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletInputSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"


class CreateDepositView(APIView):
    def post(self, reqeust, uuid, *args, **kwargs):
        data = DepositWalletInputSerializer(data=reqeust.data)
        data.is_valid(raise_exception=True)
        wallet = Wallet.objects.get(uuid=uuid)
        wallet = wallet.deposit(data.validated_data["balance"])
        return Response(WalletOutputSerializer(instance=wallet).data)


class ScheduleWithdrawView(APIView):
    def post(self, request, *args, **kwargs):
        # todo: implement withdraw logic
        pass
        return Response({})
