# Generated by Django 5.0 on 2024-11-13 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_profile_date_alter_profession_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='avatar',
            field=models.ImageField(blank=True, default='worker.jpeg', null=True, upload_to='avatar/%Y/%M/%D'),
        ),
    ]
