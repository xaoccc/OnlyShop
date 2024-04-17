from django.urls import path

from OnlyShop.payments.views import PaymentView, stripe_config, create_checkout_session, SuccessView, CancelledView, \
    stripe_webhook

urlpatterns = [
    path('<slug:payment_option>/', PaymentView.as_view(), name='order_payment'),
    path('stripe/config/', stripe_config),
    path('stripe/create-checkout-session/', create_checkout_session),
    path('stripe/success/', SuccessView.as_view()),
    path('stripe/canceled/', CancelledView.as_view()),
    path('stripe/webhook/', stripe_webhook),
]