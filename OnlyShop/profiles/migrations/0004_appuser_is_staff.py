# Generated by Django 4.2.4 on 2024-03-01 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_appuser_options_alter_appuser_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_staff',
            field=models.BooleanField(default='True'),
            preserve_default=False,
        ),
    ]
