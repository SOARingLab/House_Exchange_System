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


# 搜素聚类中心点周边1km范围内的POI分布，并进行显示
def poi_search(request):

    # 用户ID
    User_id = trace.objects.get(id=1).user_id

    # 聚类之后的类别数量
    q = trace.objects.values('cluster').distinct()
    cluster_count = q.count() - 1

    # 计算各聚类中心点坐标
    res_avg = []
    for i in range(cluster_count):
        avg_longitude = str(trace.objects.filter(cluster=i + 1).aggregate(Avg('longitude'))['longitude__avg'])
        avg_latitude = str(trace.objects.filter(cluster=i + 1).aggregate(Avg('latitude'))['latitude__avg'])
        res_avg.append([avg_longitude, avg_latitude])

    # POI候选类别
    POIs = ['美食', '酒店', '购物', '旅游景点', '休闲娱乐', '运动健身', '教育培训', '医疗', '交通设施', '金融', '住宅区', '公司企业',
            '自然地物']

    akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'

    # 存储将要传递给前端的内容
    context = {}

    # 对于每个聚类中心，分析其周边POI分布
    for i in range(cluster_count):
        cluster_POI = {}

        # 针对每个候选的POI类别
        for POI in POIs:
            url = 'http://api.map.baidu.com/place/v2/search?query=' + POI + '&location=' + res_avg[i][1] + ',' \
                  + res_avg[i][0] + '&radius=1000&output=json&ak=' + akeys

            r = requests.get(url)

            # 处理返回值
            response_dict = r.json()

            # 若果返回的结果字段不为空
            if 'results' in response_dict:
                result_trans = response_dict['results']

                # 存储查找到的该类POI的名称和地址
                loc = []

                for item in result_trans:
                    loc.append([item['name'], item['address']])

                # 对每类POI的结果进行存储
                cluster_POI[POI] = loc

            else:
                cluster_POI[POI] = 'None'

        cluster_th = 'cluster' + str(i)
        context[cluster_th] = json.dumps(cluster_POI)
        context['User_id'] = json.dumps(User_id)
    return render(request, 'UserProfile/profile.html', context)