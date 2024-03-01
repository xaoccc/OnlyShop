
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
from django.shortcuts import render, redirect

from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView, CreateView, RedirectView
from OnlyShop.main_app.models import Item, Order, ItemOrder
from OnlyShop.profiles.forms import CustomAuthenticationForm
from OnlyShop.profiles.models import AppUser


class IndexView(ListView, LoginView):
    model = Item
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = AppUser.objects.first()
        if self.request.user.is_authenticated:
            context['orders'] = Order.objects.filter(user=self.request.user, ordered=False)[0].items
        else:
            context['orders'] = 0
        return context




class UserLogIn(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    next_page = 'index'





class RegisterView(CreateView):
    model = AppUser
    template_name = 'register.html'
    fields = ['username', 'password']


# class UserLogoutView(LogoutView):
#     template_name = 'logout.html'

def user_logout(request):
    logout(request)
    return redirect('index')












