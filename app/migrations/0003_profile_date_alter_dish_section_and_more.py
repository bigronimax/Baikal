# Generated by Django 5.0 on 2024-11-10 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_dish_menu_remove_review_restaurants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='app.section'),
        ),
        migrations.AlterField(
            model_name='profession',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='professions', to='app.restaurant'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='profession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='app.profession'),
        ),
    ]
