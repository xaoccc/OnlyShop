# Generated by Django 5.0.3 on 2024-04-08 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_alter_item_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemorder',
            name='total_item_order_amount',
            field=models.FloatField(default=0),
        ),
    ]