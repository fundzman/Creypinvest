from django.contrib import admin

from users.models import Profile, Wallet, Transaction, AdminWallet, AdminTransaction

admin.site.register(AdminWallet)
admin.site.register(AdminTransaction)
admin.site.register(Profile)
admin.site.register(Wallet)
admin.site.register(Transaction)
