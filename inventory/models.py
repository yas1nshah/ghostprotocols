# from django.db import models

# # Create your models here.

# class Cities(models.Model):
#     name = models.CharField(max_length=15)


# class Makes(models.Model):
#     name = models.CharField(max_length=200)
#     logo = models.ImageField(upload_to='makes_logos/')

#     def __str__(self):
#         return self.name

# class Colors(models.Model):
#     name = models.CharField(max_length=200)

# class BodyType(models.Model):
#     name = models.CharField(max_length=200)


# class Car(models.Model):
#     make = models.ForeignKey(Makes, on_delete=models.CASCADE)
#     model = models.CharField(max_length=200)
#     year = models.IntegerField()
#     price = models.IntegerField()

#     location = models.ForeignKey(Cities, on_delete= models.CASCADE)
#     mileage = models.IntegerField(default = 0)
#     transmission = models.BooleanField(default= False)

#     # ENGINE CHOICES
#     PETROL = 'petrol'
#     DIESEL = 'diesel'
#     HYBRID = 'hybrid'
#     ENGINE_CHOICES = (
#         (PETROL, 'Petrol'),
#         (DIESEL, 'Diesel'),
#         (HYBRID, 'Hybrid'),
#     )
#     engine = models.CharField(max_length=10, choices=ENGINE_CHOICES, default= PETROL)
#     #  ENGINE CHOICE END


#     registered = models.ForeignKey(Cities, on_delete= models.CASCADE, related_name='registration')
#     Color = models.ForeignKey(Colors, on_delete= models.CASCADE )
#     body = models.ForeignKey(BodyType, on_delete= models.CASCADE)

#     # features =

#     comments = models.CharField(max_length= 1000, default="No Seller Comments")
#     # seller =

#     def __str__(self):
#         return f"{self.make.name} {self.model} ({self.year})"
