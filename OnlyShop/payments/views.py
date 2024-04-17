import logging
import stripe
from django.shortcuts import render
from django.views import View

from OnlyShop.order.models import Order
from OnlyShop.utils.mixins import GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)

PRODUCT_ID_MAP = {
    'Banana': 'prod_Pw47ZaTVgfykFY'
}


class PaymentView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'order/payment.html')



@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        line_items = []

        items = Order.objects.filter(user=request.user, ordered=False).items

        # Iterate over each item in the shopping cart
        for item in items:
            product_name = item.product.name
            quantity = item.quantity

            # Retrieve the product ID based on the product name from the mapping
            product_id = PRODUCT_ID_MAP.get(product_name)
            if not product_id:
                # Handle case where product name is not found in the mapping
                raise ValueError(f"Product '{product_name}' not found")

            # Add the product with its quantity to the line items
            line_items.append({
                'price': product_id,
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
            return JsonResponse({'sessionId': checkout_session['id']})

        except stripe.error.StripeError as e:
            logger.error("Stripe Error: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            logger.error("Unexpected Error: %s", str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


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
