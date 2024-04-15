from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
import pycountry

from OnlyShop.profiles.validators import name_validator, postal_code_validator, all_digits_validator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=(
            MinLengthValidator(2, "Your name should be minimum two characters long!"),
            name_validator,
        )
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=(
            MinLengthValidator(2, "Your name should be minimum two characters long!"),
            name_validator,
        )
    )
    profile_picture = models.URLField(blank=True, null=True)


class BillingInfo(models.Model):
    COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]
    PAYMENT_METHODS = (
        ("PayPal", "PayPal"),
        ("Stripe", "Stripe"),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=10, blank=True, null=True, validators=(postal_code_validator,))
    country = models.CharField(max_length=30, choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=30)
    street_address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=(MinLengthValidator(10), all_digits_validator))
    payment_option = models.CharField(choices=PAYMENT_METHODS)

