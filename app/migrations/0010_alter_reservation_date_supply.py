# Generated by Django 5.0 on 2024-11-13 14:24

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_review_time_alter_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(default=datetime.date(2024, 11, 13)),
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('provider', models.CharField(max_length=32)),
                ('price', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.restaurant')),
            ],
        ),
    ]
