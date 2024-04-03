from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

# Create your models here.
User_Model = get_user_model()
class Item(models.Model):
    ITEM_TYPES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Big', 'Big'),
        ('Very Big', 'Very Big'),
        ('Abstract', 'Abstract'),
    )

    LABEL_TYPES = (
        ('NEW', 'NEW'),
        ('Eco', 'Eco'),
    )

    name = models.CharField(max_length=100, verbose_name="Name")
    new_price = models.FloatField(verbose_name="Price", validators=(MinValueValidator(0, "Price must be a positive number"),))
    old_price = models.FloatField(validators=(MinValueValidator(0, "Price must be a positive number"),), blank=True, null=True)
    type = models.CharField(choices=ITEM_TYPES, max_length=20, verbose_name="Type")
    image = models.URLField(verbose_name="Image URL")
    label = models.CharField(choices=LABEL_TYPES, blank=True, null=True, max_length=10, verbose_name="Label")
    label_style = models.CharField(blank=True, null=True)
    description = models.TextField(verbose_name="Description")


    def __str__(self):
        return self.name


class ItemOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)





