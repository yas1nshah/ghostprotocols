# Generated by Django 4.1.5 on 2023-09-03 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('stockid', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('featured', models.BooleanField(default=False)),
                ('gpcar', models.BooleanField(default=False)),
                ('galleryIndex', models.IntegerField()),
                ('title', models.CharField(default='None', max_length=256)),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('price', models.IntegerField()),
                ('location', models.CharField(max_length=50)),
                ('mileage', models.IntegerField()),
                ('transmission', models.BooleanField(default=False)),
                ('engine', models.CharField(max_length=200)),
                ('engineCapacity', models.CharField(default='N/A', max_length=200)),
                ('registration', models.CharField(max_length=200)),
                ('body', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=200)),
                ('sellerComments', models.CharField(max_length=300)),
                ('seller', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DemandList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('demand', models.CharField(max_length=255)),
                ('budget', models.IntegerField()),
                ('buyer', models.CharField(max_length=255)),
                ('date', models.DateTimeField(verbose_name=django.utils.timezone.now)),
                ('done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WeSellYouWin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.car')),
            ],
        ),
    ]
