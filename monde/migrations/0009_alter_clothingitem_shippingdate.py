# Generated by Django 5.0.6 on 2024-07-22 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monde', '0008_alter_clothingitem_shippingdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothingitem',
            name='shippingDate',
            field=models.DateField(default=datetime.datetime(2024, 8, 21, 15, 56, 23, 869969)),
        ),
    ]
