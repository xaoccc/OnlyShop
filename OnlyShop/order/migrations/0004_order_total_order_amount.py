# Generated by Django 4.2.11 on 2024-03-20 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_billing_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_order_amount',
            field=models.IntegerField(default=0),
        ),
    ]