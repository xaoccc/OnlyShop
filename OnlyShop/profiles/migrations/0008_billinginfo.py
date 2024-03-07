# Generated by Django 4.2.11 on 2024-03-07 13:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(blank=True, max_length=9, null=True)),
                ('country', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('street_address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(10)])),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
    ]
