# Generated by Django 5.0.3 on 2024-04-21 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_alter_itemorder_total_item_order_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stripe_price_id',
            field=models.CharField(blank=True, default='stripe_price_id', max_length=100, null=True),
        ),
    ]
