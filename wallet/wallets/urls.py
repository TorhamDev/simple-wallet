from django.urls import path

from wallets.views import CreateDepositView, ScheduleWithdrawView, CreateWalletView, RetrieveWalletView

urlpatterns = [
    path("", CreateWalletView.as_view()),
    path("<ulid>/", RetrieveWalletView.as_view()),
    path("<ulid>/deposit", CreateDepositView.as_view()),
    path("<ulid>/withdraw", ScheduleWithdrawView.as_view()),
]
