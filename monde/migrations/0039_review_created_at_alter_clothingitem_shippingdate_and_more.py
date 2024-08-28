# Generated by Django 5.0.6 on 2024-08-01 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monde', '0038_alter_clothingitem_shippingdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='clothingitem',
            name='shippingDate',
            field=models.DateField(default=datetime.datetime(2024, 8, 31, 18, 55, 37, 767073)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bank_balance',
            field=models.FloatField(default=443.15),
        ),
    ]
