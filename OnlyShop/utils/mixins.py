from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from OnlyShop.main_app.models import Order


class OrdersCountMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and Order.objects.filter(user=self.request.user, ordered=False):
            context['orders'] = Order.objects.filter(user=self.request.user, ordered=False)[0].items
        else:
            context['orders'] = 0
        return context


class InputStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class GetUserMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class OnlyShopLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return redirect('error_401')
