from django.shortcuts import render
from django.views import View

from OnlyShop.utils.mixins import GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin


class PaymentView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'order/payment.html')
