from django.contrib import admin

from wallets.models import Transaction, Wallet

admin.site.register(Wallet)
admin.site.register(Transaction)
