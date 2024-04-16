from django.urls import path

from OnlyShop.payments.views import PaymentView

urlpatterns = [
    path('<slug:payment_option>/', PaymentView.as_view(), name='order_payment'),
]