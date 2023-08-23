# Generated by Django 4.1.5 on 2023-08-21 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('registration', models.CharField(max_length=200)),
                ('body', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=200)),
                ('sellerComments', models.CharField(max_length=300)),
                ('seller', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='inventory/images')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.car')),
            ],
        ),
    ]