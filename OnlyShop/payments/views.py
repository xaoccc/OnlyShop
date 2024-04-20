import logging
import stripe
from OnlyShop.order.models import Order
from OnlyShop.utils.mixins import GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)

PRODUCT_ID_MAP = {
    'Banana': 'price_1P7DrxP7rtsr5KNvG7c6hwuj',
    'T-Mobile': 'price_1P7FAUP7rtsr5KNvsna6X4In',
    'BLU': 'price_1P7FB7P7rtsr5KNvPdvfYWkF',
    'Nike': 'price_1P7Z4HP7rtsr5KNvSc30Ao49',
    'Adidas': 'price_1P7Z8qP7rtsr5KNvEvULYmHk',
}

class PaymentSubmitView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, TemplateView):
    template_name = 'order/payment.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/payments/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        line_items = []
        items = Order.objects.filter(user=request.user, ordered=False)[0].items.all()


        # Iterate over each item in the shopping cart
        for item in items:
            product_name = item.item.name
            quantity = item.quantity

            # Retrieve the product ID based on the product name from the mapping
            price_id = PRODUCT_ID_MAP.get(product_name)

            if not price_id:
                # Handle case where product name is not found in the mapping
                raise ValueError(f"Product '{product_name}' not found")

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

    # else:
    #     return HttpResponseNotAllowed(['GET'])


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
