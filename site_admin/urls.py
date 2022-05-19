from django.urls import path
from .views import index_view, transaction_deposit_view, transaction_del_view, transaction_accept_view

urlpatterns = [
    path("", index_view, name="admin-home"),
    path("transactions/deposit/", transaction_deposit_view,
         name="admin-transaction-deposit"),
    path("transaction/<int:id>/delete/", transaction_del_view, name="admin-transaction-delete"),
    path("transaction/<int:id>/accept/", transaction_accept_view, name="admin-transaction-accept"),
]
