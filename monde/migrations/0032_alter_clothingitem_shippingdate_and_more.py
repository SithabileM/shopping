# Generated by Django 5.0.6 on 2024-07-25 19:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monde', '0031_alter_clothingitem_shippingdate_alter_sections_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothingitem',
            name='shippingDate',
            field=models.DateField(default=datetime.datetime(2024, 8, 24, 21, 31, 14, 229404)),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='inventory',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='inventory',
            field=models.ManyToManyField(blank=True, null=True, related_name='stock', to='monde.clothingitem'),
        ),
    ]
