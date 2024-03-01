
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django import forms

from OnlyShop.profiles.models import AppUser


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Email', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']
        self.fields['email'].widget.attrs.update({'class': 'form-control active'})
        self.fields['password'].widget.attrs.update({'class': 'form-control active'})

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')


        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class CreateUserForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control active'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control active'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control active'})
