from django.db import models

# Create your models here.


# Profile数据表，存储轨迹归类分析结果
class profile(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.TextField()
    home_location = models.TextField()
    home_coordinate = models.TextField()
    work_location = models.TextField()
    work_coordinate = models.TextField()
    food_nums = models.CharField(max_length = 50)
    food_detail = models.TextField()
    hotel_nums = models.CharField(max_length = 50)
    hotel_detail = models.TextField()
    shopping_nums = models.CharField(max_length = 50)
    shopping_detail = models.TextField()
    tourism_nums = models.CharField(max_length = 50)
    tourism_detail = models.TextField()
    entertainment_nums = models.CharField(max_length = 50)
    entertainment_detail = models.TextField()
    sport_nums = models.CharField(max_length = 50)
    sport_detail = models.TextField()
    education_nums = models.CharField(max_length = 50)
    education_detail = models.TextField()
    medical_nums = models.CharField(max_length = 50)
    medical_detail = models.TextField()
    transportation_nums = models.CharField(max_length = 50)
    transportation_detail = models.TextField()
    financial_nums = models.CharField(max_length = 50)
    financial_detail = models.TextField()
    company_nums = models.CharField(max_length = 50)
    company_detail = models.TextField()
    natural_nums = models.CharField(max_length = 50)
    natural_detail = models.TextField()
    other_places = models.TextField()

# Trace表，存放原始轨迹数据集
class trace(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length = 50)
    start_time = models.CharField(max_length = 50)
    longitude = models.CharField(max_length = 50)
    latitude = models.CharField(max_length = 50)
    date = models.CharField(max_length = 50)
    cluster = models.IntegerField(default=0)
    duration = models.CharField(max_length = 50)