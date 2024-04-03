# Generated by Django 4.2.11 on 2024-04-03 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_alter_item_label_style_alter_item_new_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Big', 'Big'), ('Very Big', 'Very Big'), ('Abstract', 'Abstract')], max_length=20, verbose_name='Type'),
        ),
    ]
