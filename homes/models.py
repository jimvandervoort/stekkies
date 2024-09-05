from django.db import models

# Create your models here.
from django.db import models

class Home(models.Model):
    url = models.URLField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    photo = models.URLField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField()
    surface = models.IntegerField()
    balcony = models.BooleanField()
    bath = models.BooleanField()
    furnished = models.BooleanField()
    garden = models.BooleanField()
    description = models.TextField()
    bedrooms = models.IntegerField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.address}, {self.city}"
