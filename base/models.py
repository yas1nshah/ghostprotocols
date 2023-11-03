from django.utils import timezone
from django.db import models
from account.models import User

# Create your models here.


class Inspection(models.Model):
    rating = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} - {}'.format(self.pk, self.rating)


class Car(models.Model):
    stockid = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)

    featured = models.BooleanField(default=False)
    gpcar = models.BooleanField(default=False)

    galleryIndex = models.IntegerField()
    title = models.CharField(max_length=256, default='None')

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=200)
    year = models.IntegerField()
    price = models.IntegerField()

    location = models.CharField(max_length=50)
    mileage = models.IntegerField()
    transmission = models.BooleanField(default=False)

    engine = models.CharField(max_length=200)
    engineCapacity = models.CharField(max_length=200, default='N/A')
    registration = models.CharField(max_length=200)
    body = models.CharField(max_length=200)
    color = models.CharField(max_length=200)

    # Change the field type to OneToOneField
    inspection = models.OneToOneField(
        Inspection, on_delete=models.CASCADE, null=True, blank=True)

    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1)
    sellerComments = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        # Generate title field from other fields on each model creation/edit
        self.title = f"{self.make} {self.model} {self.year}"

        # Run default Django implementation for save method
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.pk, self.make, self.model, self.year)


class Gallery(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, null=False, to_field='stockid')
    image = models.ImageField(upload_to='images')


class CarReports(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, null=False, to_field='stockid')
    reason = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)


class WeSellYouWin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class DemandList(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    demand = models.CharField(max_length=255)
    budget = models.IntegerField()
    buyer = models.CharField(max_length=255)
    date = models.DateTimeField(timezone.now)
    done = models.BooleanField(default=False)
