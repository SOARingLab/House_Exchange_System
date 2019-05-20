from django.db import models

# Create your models here.

class trace(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length = 50)
    start_time = models.CharField(max_length = 50)
    longitude = models.CharField(max_length = 50)
    latitude = models.CharField(max_length = 50)
    date = models.CharField(max_length = 50)
    cluster = models.IntegerField()
