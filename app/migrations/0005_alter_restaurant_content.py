# Generated by Django 5.0 on 2024-11-21 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_restaurant_content_alter_restaurant_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='content',
            field=models.CharField(default='', max_length=200),
        ),
    ]
