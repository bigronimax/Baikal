# Generated by Django 5.0 on 2024-11-15 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_order_profile_order_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='guests',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(default=datetime.date(2024, 11, 15)),
        ),
    ]
