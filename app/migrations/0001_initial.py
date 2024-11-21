# Generated by Django 5.0 on 2024-11-20 22:11

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('content', models.TextField(max_length=32)),
                ('price', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('img', models.ImageField(blank=True, default='dish.webp', null=True, upload_to='dish_image/%Y/%M/%D')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=32)),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=12, null=True, validators=[django.core.validators.RegexValidator(message='Invalid format', regex='^\\+?[7,8]?[\\s,-]?\\(?\\d{3}\\)?[\\s,-]?\\d{3}[\\s,-]?\\d{2}[\\s,-]?\\d{2}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Комбо', 'Комбо'), ('Закуски', 'Закуски'), ('Горячее', 'Горячее')], default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('dish', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='app.dish')),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Официанты', 'Официанты'), ('Повара', 'Повара'), ('Менеджеры', 'Менеджеры')], default='', max_length=10)),
                ('restaurant', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='professions', to='app.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='avatar.png', null=True, upload_to='avatar/%Y/%M/%D')),
                ('user', models.OneToOneField(default='', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.IntegerField(default=1, null=True)),
                ('guests', models.IntegerField(default=1, null=True)),
                ('date', models.DateTimeField(null=True)),
                ('restaurant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='app.restaurant')),
                ('dishes', models.ManyToManyField(blank=True, to='app.orderdish')),
                ('profile', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid format', regex='^\\+?[7,8]?[\\s,-]?\\(?\\d{3}\\)?[\\s,-]?\\d{3}[\\s,-]?\\d{2}[\\s,-]?\\d{2}$')])),
                ('guests', models.IntegerField(choices=[(1, '1 гость'), (2, '2 Гостя'), (3, '3 Гостя'), (4, '4 Гостя'), (5, '5 Гостей'), (6, '6 Гостей')], default='')),
                ('date', models.DateField(default=datetime.date(2024, 11, 20))),
                ('time', models.TimeField(choices=[(datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00')], default='')),
                ('comment', models.TextField(blank=True, max_length=100, null=True)),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(max_length=200)),
                ('date', models.DateTimeField(null=True)),
                ('verdict', models.CharField(choices=[('Удивительно!', 'Удивительно!'), ('Хорошо!', 'Хорошо!'), ('Плохо!', 'Плохо!'), ('Ужасно!', 'Ужасно!')], default='', max_length=15)),
                ('profile', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='app.section'),
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('provider', models.CharField(max_length=32)),
                ('price', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('restaurant', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='app.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField()),
                ('profession', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='app.profession')),
                ('profile', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='app.profile')),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='app.menu'),
        ),
    ]
