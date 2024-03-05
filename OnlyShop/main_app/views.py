from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from OnlyShop.main_app.models import Item, Order, ItemOrder
from django.contrib import messages
from OnlyShop.utils.mixins import OrdersCountMixin


class ItemDetailView(OrdersCountMixin, DetailView):
    model = Item
    template_name = 'product/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_items'] = Item.objects.exclude(id=self.object.id)[:3]
        context['user'] = self.request.user
        return context


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = ItemOrder.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        order = order_queryset[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Your order was updated.")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)

    else:
        ordered_at = timezone.now()
        order = Order.objects.create(user=request.user, created_at=ordered_at)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")

    return redirect("item-details", pk=pk)


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        order = order_queryset[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = ItemOrder.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
        else:
            messages.info(request, "The order does not contain this item.")
            return redirect("item-details", pk=pk)

    else:
        messages.info(request, "There is no order yet.")
        return redirect("item-details", pk=pk)

    return redirect("item-details", pk=pk)


class ItemCreateView(OrdersCountMixin, CreateView):
    template_name = 'add_item.html'
    model = Item
    fields = ['name', 'new_price', 'old_price', 'type', 'label', 'label_style', 'image', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        return reverse('index')





