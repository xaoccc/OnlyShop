from django.db import models
from django.conf import settings

# Create your models here.
class Item(models.Model):
    ITEM_TYPES = (
        ('Shirt', 'Shirt'),
        ('Outwear', 'Outwear'),
        ('Sport wear', 'Sport wear'),
    )

    LABEL_TYPES = (
        ('NEW', 'NEW'),
        ('Eco', 'Eco'),
    )

    LABEL_STYLES = (
        ('bg-dark', 'bg-dark'),
        ('bg-success', 'bg-success'),
    )

    name = models.CharField(max_length=100)
    new_price = models.FloatField()
    old_price = models.FloatField(blank=True, null=True)
    type = models.CharField(choices=ITEM_TYPES, max_length=20)
    image = models.URLField()
    label = models.CharField(choices=LABEL_TYPES, blank=True, null=True, max_length=10)
    label_style = models.CharField(choices=LABEL_STYLES, blank=True, null=True, max_length=10)
    description = models.TextField(verbose_name="Description")


    def __str__(self):
        return self.name


class ItemOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(ItemOrder)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.user.username


