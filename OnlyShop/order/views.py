from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView, FormView

from OnlyShop.main_app.models import ItemOrder
from OnlyShop.order.models import Order
from OnlyShop.profiles.forms import BillingInfoForm
from OnlyShop.profiles.models import BillingInfo
from OnlyShop.utils.mixins import OrdersCountMixin, OnlyShopLoginRequiredMixin, GetUserMixin


# Create your views here.


class AllOrdersView(OnlyShopLoginRequiredMixin, OrdersCountMixin, ListView):
    model = Order
    template_name = "order/all-orders.html"

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user, ordered=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["billing_info"] = BillingInfo.objects.filter(profile=self.request.user.profile)

        for order in Order.objects.filter(user=self.request.user):
            for item in order.items.all():
                order.total_order_amount += item.quantity * item.item.new_price
            order.save()

        return context

class OrderDetailsView(OnlyShopLoginRequiredMixin, OrdersCountMixin, DetailView):
    model = Order
    template_name = "order/order-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.object.items

        return context


class OrderCompleteView(OnlyShopLoginRequiredMixin, OrdersCountMixin, TemplateView):
    template_name = "order/order-success.html"


class NoOrdersView(OnlyShopLoginRequiredMixin, OrdersCountMixin, TemplateView):
    template_name = "order/order-unavailable.html"


class OrderSummaryView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order-summary.html'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, ordered=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cart_amount = 0
        if Order.objects.filter(user=self.request.user, ordered=False):
            for item in Order.objects.filter(user=self.request.user, ordered=False)[0].items.all():
                total_cart_amount += item.item.new_price * item.quantity
        context['total_cart_amount'] = total_cart_amount
        context['current_order'] = Order.objects.filter(user=self.request.user)
        return context


class OrderCheckoutView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, FormView):
    template_name = 'order/order-checkout.html'
    form_class = BillingInfoForm
    def get_success_url(self):
        return reverse('order_completed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cart_amount = 0
        if Order.objects.filter(user=self.request.user, ordered=False):
            for item in Order.objects.filter(user=self.request.user, ordered=False)[0].items.all():
                total_cart_amount += item.item.new_price * item.quantity
        context['total_cart_amount'] = total_cart_amount
        context['current_order'] = Order.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        billing_info_form = BillingInfoForm(request.POST, user_profile=request.user.profile)
        if not self.request.user.profile.first_name or not self.request.user.profile.last_name:
            return redirect('profile-edit', pk=self.request.user.profile.pk)

        if billing_info_form.is_valid():
            if not Order.objects.filter(user=self.request.user, ordered=False):
                return redirect('order_unavailable')

            billing_info_form.save()
            current_billing_info = BillingInfo.objects.last()
            current_order = Order.objects.filter(user=self.request.user, ordered=False)[0]
            current_order.ordered = True
            current_order.billing_info = current_billing_info
            total_cart_amount = 0
            if Order.objects.filter(user=self.request.user, ordered=False):
                for item in Order.objects.filter(user=self.request.user, ordered=False)[0].items.all():
                    total_cart_amount += item.item.new_price * item.quantity

            current_order.total_order_amount = total_cart_amount
            current_order.save()
            return redirect('order_completed')
        else:
            context = self.get_context_data()
            return self.render_to_response(context)

