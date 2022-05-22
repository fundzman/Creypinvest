from django.urls import path
from .views import (deposit, deposit_amount,
                    deposit_amount_auth, deposit_window, deposit_done, withdraw_window, withdraw_done)

urlpatterns = [
    path("deposit/", deposit, name="deposit"),
    path("deposit/<str:pack>/", deposit_amount, name="deposit_amount"),
    path("deposit/<str:pack>/auth/", deposit_amount_auth,
         name="deposit_amount_auth"),
    path("deposit/auth/start-window/", deposit_window, name="deposit_window"),
    path("deposit/<str:plan>/auth/done/", deposit_done, name="deposit_done"),

    path("withdraw/auth/start-window/", withdraw_window, name="withdraw_window"),
    path("withdraw/debit/auth/done/", withdraw_done, name="withdraw_done"),
    # deposit_amount_auth
]
