
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, TemplateView, CreateView, RedirectView
from OnlyShop.main_app.models import Item, Order, ItemOrder
from OnlyShop.profiles.forms import CustomAuthenticationForm, CreateUserForm
from OnlyShop.profiles.models import AppUser


class IndexView(ListView):
    model = Item
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        if self.request.user.is_authenticated and Order.objects.filter(user=self.request.user, ordered=False):
            context['orders'] = Order.objects.filter(user=self.request.user, ordered=False)[0].items
        else:
            context['orders'] = 0
        return context




class UserLogIn(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    next_page = 'index'



class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'register.html'

    def form_valid(self, form):
        form.instance.password = make_password(form.cleaned_data['password'])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


def user_logout(request):
    request.user = AnonymousUser()
    logout(request)
    return redirect('index')












