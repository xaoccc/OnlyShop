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
    fields = ['name', 'new_price', 'old_price', 'type', 'label', 'label_style', 'image', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_success_url(self):
        return reverse('index')


class ItemEditView(OrdersCountMixin, OnlyShopStaffRequiredMixin, UpdateView):
    model = Item
    template_name = "item/item-edit.html"
    fields = ["name", "old_price", "new_price", "type", "image", "label", "description"]

    def get_success_url(self):
        return reverse('item-details', kwargs={'pk': self.object.pk})


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


class OrderSummaryView(GetUserMixin, OrdersCountMixin, OnlyShopLoginRequiredMixin, ListView, FormView):
    model = Order
    template_name = 'checkout.html'
    form_class = BillingInfoForm
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

    def post(self, request, *args, **kwargs):
        billing_info_form = BillingInfoForm(request.POST, user_profile=request.user.profile)

        if billing_info_form.is_valid():
            billing_info_form.save()
            current_billing_info = BillingInfo.objects.last()
            if not Order.objects.filter(user=self.request.user, ordered=False):
                return redirect('order_unavailable')

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if BillingInfo.objects.filter(profile=self.request.user.profile):
            last_instance = BillingInfo.objects.filter(profile=self.request.user.profile).last()
            kwargs['instance'] = last_instance
        return kwargs










