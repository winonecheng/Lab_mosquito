from django.db import models

# Create your models here.
class User(models.Model):
	state = models.IntegerField(default=0)
	uid = models.CharField(max_length=200)
	temperature = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	latitude = models.CharField(max_length=200)
	longitude = models.CharField(max_length=200)
