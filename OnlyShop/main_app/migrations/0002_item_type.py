# Generated by Django 4.2.4 on 2024-02-23 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(blank=True, choices=[('Shirt', 'Shirt'), ('Outwear', 'Outwear'), ('Sport wear', 'Sport wear')], max_length=50, null=True),
        ),
    ]
