# Generated by Django 5.0.6 on 2024-07-25 17:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monde', '0029_alter_clothingitem_shippingdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='clothingitem',
            name='sections',
        ),
        migrations.AlterField(
            model_name='clothingitem',
            name='shippingDate',
            field=models.DateField(default=datetime.datetime(2024, 8, 24, 19, 49, 40, 838343)),
        ),
        migrations.AddField(
            model_name='clothingitem',
            name='clothingSections',
            field=models.ManyToManyField(max_length=100, to='monde.sections'),
        ),
    ]
