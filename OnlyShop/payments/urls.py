from django.urls import path

from OnlyShop.payments.views import stripe_config, create_checkout_session, SuccessView, CancelledView, \
    stripe_webhook, PaymentSubmitView

urlpatterns = [
    path('', PaymentSubmitView.as_view(), name='payment_submit'),
    path('stripe/config/', stripe_config),
    path('stripe/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('success/', SuccessView.as_view()),
    path('cancelled/', CancelledView.as_view()),
    path('stripe/webhook/', stripe_webhook),
]