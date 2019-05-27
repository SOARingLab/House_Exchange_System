import json
import requests
from UserProfile.models import trace
from django.db.models import Avg

# 搜素聚类中心点周边1km范围内的POI分布
def poi_search():

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

    for i in range(cluster_count):
        cluster_POI = {}

        for POI in POIs:
            url = 'http://api.map.baidu.com/place/v2/search?query=' + POI + '&location=' + res_avg[i][1] + ',' \
                  + res_avg[i][0] + '&radius=1000&output=json&ak=' + akeys

            r = requests.get(url)

            # 处理返回值
            response_dict = r.json()

            if 'results' in response_dict:
                result_trans = response_dict['results']

                # 存储查找到的该类POI名称和地址
                loc = []

                for item in result_trans:
                    loc.append([item['name'], item['address']])
                cluster_POI[POI] = loc

            else:
                cluster_POI[POI] = 'None'

            print(POI + 'finished')


        cluster_th = 'cluster' + str(i)
        context[cluster_th] = json.dumps(cluster_POI)

        print(cluster_th + 'finished')

    print(context)

poi_search()


