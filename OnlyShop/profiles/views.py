from django.contrib.auth import logout, get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from OnlyShop.main_app.models import Item, Order, ItemOrder
from OnlyShop.profiles.forms import UserLoginForm, CreateUserForm
from OnlyShop.utils.mixins import OrdersCountMixin, GetUserMixin

UserModel = get_user_model()



class IndexView(GetUserMixin, OrdersCountMixin, ListView):
    model = Item
    template_name = 'index.html'
    paginate_by = 8



class OrderSummaryView(GetUserMixin, OrdersCountMixin,  ListView):
    model = Order
    template_name = 'checkout.html'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, ordered=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cart_amount = 0
        for item in Order.objects.filter(user=self.request.user, ordered=False)[0].items.all():
            total_cart_amount += item.item.new_price * item.quantity

        context['total_cart_amount'] = total_cart_amount
        return context


class UserLogIn(LoginView):
    authentication_form = UserLoginForm
    template_name = 'login.html'


class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'register.html'
    def get_success_url(self):
        return reverse('index')

    def form_valid(self, *args, **kwargs):
        form = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return form

def user_logout(request):
    logout(request)
    return redirect('index')












