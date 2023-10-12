from django.db import models


status_choices = [('Active','Active'),('Inactive','Inactive')]

# Create your models here.
class LocationHub(models.Model):
    location_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=10, choices=status_choices, default='Active')

    def __str__(self):
        return self.location_name