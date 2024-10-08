# Generated by Django 5.0.6 on 2024-07-25 19:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monde', '0032_alter_clothingitem_shippingdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothingitem',
            name='shippingDate',
            field=models.DateField(default=datetime.datetime(2024, 8, 24, 21, 33, 34, 532724)),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cart_items',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='inventory',
            field=models.ManyToManyField(blank=True, related_name='stock', to='monde.clothingitem'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cart_items',
            field=models.ManyToManyField(blank=True, to='monde.clothingitem'),
        ),
    ]
