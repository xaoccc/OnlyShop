from django.contrib.auth.models import User
from django.http import request
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView
from OnlyShop.main_app.models import Item, Order, ItemOrder
from OnlyShop.profiles.models import AppUser


class IndexView(ListView):
    model = Item
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = AppUser.objects.first()
        context['orders'] = Order.objects.filter(user=self.request.user, ordered=False)[0].items
        return context


