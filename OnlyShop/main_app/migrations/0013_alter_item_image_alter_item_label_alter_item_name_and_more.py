# Generated by Django 4.2.11 on 2024-03-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_item_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.URLField(verbose_name='Image URL'),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('NEW', 'NEW'), ('Eco', 'Eco')], max_length=10, null=True, verbose_name='Label'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='item',
            name='new_price',
            field=models.FloatField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('Shirt', 'Shirt'), ('Outwear', 'Outwear'), ('Sport wear', 'Sport wear')], max_length=20, verbose_name='Type'),
        ),
    ]
