from django.db import models

class User(models.Model):
    state = models.IntegerField(default=0)
    uid = models.CharField(max_length=200)
    temperature = models.FloatField(default=0)
    address = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    report_date = models.DateTimeField()

    def __str__(self):
        return self.uid

class Dengue(models.Model):
    address = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date)

class Flu(models.Model):
    address = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date)