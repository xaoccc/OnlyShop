from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, FormView, TemplateView
from OnlyShop.main_app.forms import ItemDeleteForm
from OnlyShop.main_app.models import Item, ItemOrder
from django.contrib import messages

from OnlyShop.order.models import Order
from OnlyShop.profiles.forms import BillingInfoForm
from OnlyShop.profiles.models import BillingInfo
from OnlyShop.utils.mixins import OrdersCountMixin, GetUserMixin, OnlyShopStaffRequiredMixin, OnlyShopLoginRequiredMixin


class ItemDetailView(OrdersCountMixin, LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'item/item-details.html'

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


class ItemCreateView(OrdersCountMixin, OnlyShopStaffRequiredMixin, CreateView):
    template_name = 'item/item-add.html'
    model = Item
    fields = ['name', 'new_price', 'old_price', 'type', 'label', 'image', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        label_value = form.cleaned_data['label']

        if label_value == 'NEW':
            label_style = 'bg-primary'
        elif label_value == 'Eco':
            label_style = 'bg-success'
        else:
            label_style = None

        instance = form.save(commit=False)
        instance.label_style = label_style
        instance.save()

        return super().form_valid(form)


class ItemEditView(OrdersCountMixin, OnlyShopStaffRequiredMixin, UpdateView):
    model = Item
    template_name = "item/item-edit.html"
    fields = ["name", "old_price", "new_price", "type", "image", "label", "description"]

    def get_success_url(self):
        return reverse('item-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        label_value = form.cleaned_data['label']

        if label_value == 'NEW':
            label_style = 'bg-primary'
        elif label_value == 'Eco':
            label_style = 'bg-success'
        else:
            label_style = None

        instance = form.save(commit=False)
        instance.label_style = label_style
        instance.save()

        return super().form_valid(form)


class ItemDeleteView(OnlyShopStaffRequiredMixin, OrdersCountMixin, DeleteView):
    # We cannot use both model and form, we must choose one of them
    # As you can see, we use the model for the DeleteView, not the form
    # form_valid in the BaseDeleteView deletes the model instance.
    model = Item
    template_name = "item/item-delete.html"
    success_url = reverse_lazy('index')

    # Here we use only the data (values and labels) from the form. The submission uses the model!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemDeleteForm(initial=self.object.__dict__)
        return context











