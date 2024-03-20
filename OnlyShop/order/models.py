from django.contrib.auth import get_user_model
from django.db import models
from OnlyShop.main_app.models import ItemOrder
from OnlyShop.profiles.models import BillingInfo

User_Model = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE)
    billing_info = models.ForeignKey(BillingInfo, blank=True, null=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(ItemOrder)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField()
    total_order_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Order {self.pk} of user {self.user}"
