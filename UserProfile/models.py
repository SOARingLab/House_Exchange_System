from django.db import models

# Create your models here.


# Profile数据表，存储轨迹归类分析结果
class profile(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length = 500)
    home_location = models.CharField(max_length = 500)
    home_coordinate = models.CharField(max_length = 500)
    work_location = models.CharField(max_length = 500)
    work_coordinate = models.CharField(max_length = 500)
    food_nums = models.IntegerField()
    food_detail = models.CharField(max_length = 500)
    hotel_nums = models.IntegerField()
    hotel_detail = models.CharField(max_length = 500)
    shopping_nums = models.IntegerField()
    shopping_detail = models.CharField(max_length = 500)
    tourism_nums = models.IntegerField()
    tourism_detail = models.CharField(max_length = 500)
    entertainment_nums = models.IntegerField()
    entertainment_detail = models.CharField(max_length = 500)
    sport_nums = models.IntegerField()
    sport_detail = models.CharField(max_length = 500)
    education_nums = models.IntegerField()
    education_detail = models.CharField(max_length = 500)
    medical_nums = models.IntegerField()
    medical_detail = models.CharField(max_length = 500)
    transportation_nums = models.IntegerField()
    transportation_detail = models.CharField(max_length = 500)
    financial_nums = models.IntegerField()
    financial_detail = models.CharField(max_length = 500)
    company_nums = models.IntegerField()
    company_detail = models.CharField(max_length = 500)
    natural_nums = models.IntegerField()
    natural_detail = models.CharField(max_length = 500)
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