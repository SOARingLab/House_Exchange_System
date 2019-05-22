from django.shortcuts import render
from .models import trace
import json
import requests
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
# 原始轨迹
def raw(request):
    dataall = trace.objects.all()

    res = []
    for data in dataall:
        curr = [data.id, data.user_id, data.start_time, data.longitude, data.latitude, data.date, data.cluster]
        res.append(curr)

    context = {'trace':json.dumps(res)}

    return render(request, 'UserProfile/raw.html',context)

# 聚类后的轨迹
def clustering(request):

    # 聚类之后的类别数量
    q = trace.objects.values('cluster').distinct()
    cluster_count = q.count() - 1
    data = []
    data_transform = []

    # 按类别提取轨迹数据
    for i in range(1, cluster_count+1):
        data.append(trace.objects.filter(cluster = i))

    # 对提取的轨迹数据进行解析，构造成可以用json格式传送的形式
    for item in data:
        res = []
        for traces_data in item:
            curr = [traces_data.id, traces_data.user_id, traces_data.start_time, traces_data.longitude,
                    traces_data.latitude, traces_data.date, traces_data.cluster]
            res.append(curr)
        data_transform.append(res)

    # 计算各聚类中心点坐标
    res_avg = []
    for i in range(cluster_count):
        avg_longitude = str(trace.objects.filter(cluster = i+1).aggregate(Avg('longitude'))['longitude__avg'])
        avg_latitude = str(trace.objects.filter(cluster = i+1).aggregate(Avg('latitude'))['latitude__avg'])
        res_avg.append([avg_longitude, avg_latitude])

    context = {'trace': json.dumps(data_transform), 'cluster_center': json.dumps(res_avg)}

    return render(request, 'UserProfile/clustering.html', context)

# 用户档案页面
def profile(request):
    User_id = trace.objects.get(id = 1)

    id = User_id.user_id
    res_ave1 = [str(121.0731659785081), str(30.167830507953518)]
    res_ave2 = [str(121.16122647825613), str(30.05795804264899)]
    res_ave3 = [str(121.6157937789176), str(29.863626306675116)]

    context = {'User_id':json.dumps(id), 'ave1': json.dumps(res_ave1), 'ave2': json.dumps(res_ave2),
               'ave3': json.dumps(res_ave3)}

    return render(request, 'UserProfile/profile.html', context)

# 搜素聚类中心点周边1km范围内的POI分布
def poi_search(request):

    # POI类别
    POIs = ['银行','商场','酒店','超市','邮局','电影院','小学','公交车站','体育场馆']
    akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'

    # 存储将要传递给前端的内容
    context = {}

    for POI in POIs:
        url = 'http://api.map.baidu.com/place/v2/search?query=' + POI + '&location=29.863626306675116,121.6157937789176&' \
                                                                     'radius=1000&output=json&ak=' + akeys
        r = requests.get(url)

        # 处理返回值
        response_dict = r.json()
        result_trans = response_dict['results']

        # 存储查找到的该类POI名称
        loc_name = []

        for item in result_trans:
            loc_name.append(item['name'])
        context[POI] = json.dumps(loc_name)

    return render(request, 'UserProfile/profile.html', context)