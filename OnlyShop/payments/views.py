import logging
import os

import stripe
from OnlyShop.order.models import Order
from OnlyShop.profiles.models import BillingInfo
from OnlyShop.utils.mixins import GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)

class PaymentSubmitView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, TemplateView):
    template_name = 'payment/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = []
        if Order.objects.filter(user=self.request.user, ordered=False):
            for item in Order.objects.filter(user=self.request.user, ordered=False)[0].items.all():
                if not item.ordered:
                    items.append(item)

        context['items'] = items
        context['billing_info'] = BillingInfo.objects.filter(profile=self.request.user.profile).last()
        return context


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = os.environ.get('STRIPE_DOMAIN_URL')
        stripe.api_key = settings.STRIPE_SECRET_KEY

        line_items = []
        items = Order.objects.filter(user=request.user, ordered=False)[0].items.all()

        # Iterate over each item in the shopping cart
        for item in items:
            # Here we connect unique item from our app (product_id) with unique item from our stripe account (price_id)
            # Make sure that the item name and item price is the same in both the app and stripe account
            product_id = item.item.id
            quantity = item.quantity
            price_id = item.item.stripe_price_id

            if not price_id:
                raise ValueError(f"Product with id '{product_id}' not found")

            # Add the product with its quantity to the line items
            line_items.append({
                'price': price_id,
                'quantity': quantity,
            })

        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items
            )
            # Update the items in the cart to be ordered
            items_in_cart = Order.objects.filter(user=request.user, ordered=False)[0].items.all()
            for item in items_in_cart:
                item.ordered = True
                item.save()
            # Update the order status at the last possible place in the code
            Order.objects.filter(user=request.user, ordered=False).update(ordered=True)
            return JsonResponse({'sessionId': checkout_session['id']})

        except stripe.error.StripeError as e:
            logger.error("Stripe Error: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            logger.error("Unexpected Error: %s", str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


class SuccessView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, TemplateView):
    template_name = 'payment/success.html'


class CancelledView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, TemplateView):
    template_name = 'payment/canceled.html'


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)
