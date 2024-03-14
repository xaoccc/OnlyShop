from django.contrib.auth import logout, get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from OnlyShop.main_app.models import Item, Order, ItemOrder
from OnlyShop.profiles.forms import UserLoginForm, CreateUserForm, ProfileEditForm, UserDeleteForm
from OnlyShop.profiles.models import Profile
from OnlyShop.utils.mixins import OrdersCountMixin, GetUserMixin, OnlyShopLoginRequiredMixin

UserModel = get_user_model()


class IndexView(GetUserMixin, OrdersCountMixin, ListView):
    model = Item
    template_name = 'index.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = Item.objects.all()
        filter_by_item_name = self.request.GET.get("item_name", None)

        if filter_by_item_name:
            queryset = queryset.filter(name__icontains=filter_by_item_name)

        filter_by_item_type = self.request.GET.get("item_type", None)
        if filter_by_item_type:
            queryset = Item.objects.filter(type__iexact=filter_by_item_type)

        return queryset


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
        # Here we log in the newly registered user and he/she/it is redirected
        # to the home page as legged-in user for better UX
        login(self.request, self.object)
        return form

def user_logout(request):
    logout(request)
    return redirect('index')


class ProfileDetailView(OnlyShopLoginRequiredMixin, OrdersCountMixin, DetailView):
    template_name = 'profile/profile-details.html'
    model = Profile

class ProfileEditView(OnlyShopLoginRequiredMixin, OrdersCountMixin, UpdateView):
    template_name = 'profile/profile-edit.html'
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Profile.objects.all()

class ProfileDeleteView(OnlyShopLoginRequiredMixin, OrdersCountMixin, DeleteView):
    template_name = 'profile/profile-delete.html'
    form_class = UserDeleteForm

    def get_success_url(self):
        return reverse('index')

    def get_queryset(self):
        return UserModel.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

class Error_401(TemplateView):
    template_name = "401.html"







