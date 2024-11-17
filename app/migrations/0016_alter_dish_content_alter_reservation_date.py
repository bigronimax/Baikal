# Generated by Django 5.0 on 2024-11-14 00:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_dish_isenable_dish_img_alter_restaurant_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='content',
            field=models.TextField(max_length=32),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(default=datetime.date(2024, 11, 14)),
        ),
    ]