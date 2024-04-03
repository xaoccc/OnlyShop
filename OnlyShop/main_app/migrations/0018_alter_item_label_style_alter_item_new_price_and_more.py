# Generated by Django 4.2.11 on 2024-04-03 12:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label_style',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='new_price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0, 'Price must be a positive number')], verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='old_price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, 'Price must be a positive number')]),
        ),
    ]
