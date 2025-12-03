from django.urls import path
from .views import transaction_list, transaction_detail

urlpatterns = [
    path("transactions/", transaction_list, name="transactions"),
    path("transactions/<int:id>/", transaction_detail, name="transaction-detail"),
]
