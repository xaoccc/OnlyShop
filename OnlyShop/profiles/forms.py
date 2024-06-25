from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django import forms
from django.core.validators import MinLengthValidator

from OnlyShop.profiles.models import Profile, BillingInfo
from OnlyShop.profiles.validators import name_validator
from OnlyShop.utils.mixins import InputStyleMixin

UserModel = get_user_model()


class UserLoginForm(InputStyleMixin, AuthenticationForm):
    email = forms.EmailField(label='Email', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

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


class CreateUserForm(InputStyleMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2']

    # Here we create a new Profile instance automatically when creating a user
    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(user=user)
        if commit:
            profile.save()
        return user


class ProfileEditForm(InputStyleMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # Add validators to the fields
        self.fields['first_name'].validators += [MinLengthValidator(2, "Your name should be minimum two characters long!"), name_validator]
        self.fields['last_name'].validators += [MinLengthValidator(2, "Your name should be minimum two characters long!"), name_validator]



class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(UserDeleteForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = ['readonly']


class BillingInfoForm(forms.ModelForm):
    class Meta:
        model = BillingInfo
        fields = ["postal_code", "country", "city", "street_address", "phone_number"]

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if BillingInfo.objects.filter(profile=user_profile):
            self.instance = BillingInfo.objects.filter(profile=user_profile).last()
        else:
            self.instance.profile = user_profile


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



