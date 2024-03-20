from django.views.generic import ListView, DetailView, TemplateView
from OnlyShop.order.models import Order
from OnlyShop.profiles.models import BillingInfo
from OnlyShop.utils.mixins import OrdersCountMixin, OnlyShopLoginRequiredMixin


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

        return context

class OrderDetailView(OnlyShopLoginRequiredMixin, OrdersCountMixin, DetailView):
    model = Order
    template_name = "order/order-details.html"


class OrderCompleteView(OnlyShopLoginRequiredMixin, OrdersCountMixin, TemplateView):
    template_name = "order/order-success.html"
