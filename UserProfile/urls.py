from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.raw, name='raw'),
    re_path(r'^clustering/$', views.clustering, name='clustering'),
    re_path(r'^profile/$', views.poi_search, name='profile'),
]