from django.db import models

# Create your models here.


class Destination(models.Model):
    
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    typeofplace=models.CharField(max_length=200)
    #price = models.IntegerField()
    #offer = models.BooleanField(default=False)
    objects=models.Manager()
