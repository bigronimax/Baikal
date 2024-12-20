# Generated by Django 5.0 on 2024-11-21 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_restaurant_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='content',
            field=models.TextField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='img',
            field=models.ImageField(blank=True, default='background.jpg', null=True, upload_to='restaurant_image/%Y/%M/%D'),
        ),
    ]
