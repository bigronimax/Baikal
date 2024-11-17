# Generated by Django 5.0 on 2024-11-14 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_dish_content_alter_reservation_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='review',
            name='verdict',
            field=models.CharField(choices=[('Удивительно!', 'Удивительно!'), ('Хорошо!', 'Хорошо!'), ('Плохо!', 'Плохо!'), ('Ужасно!', 'Ужасно!')], default='', max_length=15),
        ),
    ]
