# Generated by Django 5.0.6 on 2024-07-23 21:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monde', '0025_alter_clothingitem_shippingdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='clothingitem',
            name='shippingDate',
            field=models.DateField(default=datetime.datetime(2024, 8, 22, 23, 20, 46, 958821)),
        ),
    ]
