# Generated by Django 5.0.3 on 2024-04-08 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_total_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_order_amount',
            field=models.FloatField(default=0),
        ),
    ]