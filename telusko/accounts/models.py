from django.db import models
from django.contrib.auth.models import  User

class CustomPreferences(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='custom')
    preferences = models.TextField(max_length=120,blank=True,default='beaches')
    objects=models.Manager()

    def __str__(self):
        return self.user.username
# Create your models here.
