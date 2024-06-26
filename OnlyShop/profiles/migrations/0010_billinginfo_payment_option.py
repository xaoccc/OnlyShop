# Generated by Django 4.2.11 on 2024-04-15 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_alter_billinginfo_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billinginfo',
            name='payment_option',
            field=models.CharField(choices=[('PayPal', 'PayPal'), ('Stripe', 'Stripe')], default='PayPal'),
            preserve_default=False,
        ),
    ]
