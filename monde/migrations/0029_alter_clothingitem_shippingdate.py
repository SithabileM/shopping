# Generated by Django 5.0.6 on 2024-07-25 17:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monde', '0028_clothingitem_sections_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothingitem',
            name='shippingDate',
            field=models.DateField(default=datetime.datetime(2024, 8, 24, 19, 40, 13, 162741)),
        ),
    ]
