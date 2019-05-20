from django.shortcuts import render
from .models import trace
import json
import pandas as pd
import numpy as np
import time
import requests
import math
import pymysql
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

# 对整个数据集按照用户ID分类，再按照产生时间进行排序
def dataset_merge():
    data_merge = pd.DataFrame()

    for i in range(1, 13):
        # 文件名
        if i < 10:
            file_name = 'DataTech_Public_Trace_0' + str(i)
        else:
            file_name = 'DataTech_Public_Trace_' + str(i)
        # 读入文件
        data = pd.read_table(file_name, sep='|', names=['USER_ID', 'START_TIME', 'LONGITUDE', 'LATITUDE', 'date'])
        # 数据合并
        data_merge = pd.concat([data_merge, data])
        print('the {}th dataset joined......'.format(i))

    # 以ID为基准进行分组
    grouped = data_merge.groupby('USER_ID')
    # 储存每个ID对应的所有记录
    for name, group in grouped:
        group = group.sort_values(by=['START_TIME'])
        group.to_csv('cleaned_data/{}.csv'.format(name), index=False)
        print('User ID:{} completed......'.format(name))

    print('Finished!!!')

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

# 将数据集原始坐标转换为百度地图坐标
def coordinate_trans():
    # 时间戳
    timestamp_start = time.time()

    data = pd.read_csv('cleaned_data/0a0aaa2c5802f17d89ac93dc57633b76.csv')

    # 经纬度坐标集
    coordinate = data[['LONGITUDE', 'LATITUDE']].astype(str).values

    # AK
    akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'

    # 数据集长度
    len_data = len(data)

    # 已转换数
    k_trans = 0
    # 循环次数
    count = 0

    # 转换后的经纬度
    longitude_trans = []
    latitude_trans = []

    # 单次请求的最大数量
    max_trans = 100

    # 构建http请求转换原坐标为百度地图坐标
    while k_trans <= len_data:
        # http请求的url字符串
        str_trans = ''
        # 每批待转换的index
        index_trans = np.arange(0)

        # 每次批量转换100个坐标
        # 判断剩余未转换坐标数量
        if len_data - k_trans <= max_trans:
            index_trans = np.arange(k_trans, len_data)
        else:
            index_trans = np.arange(k_trans, k_trans + max_trans)

        # 构建请求字符串
        for i in index_trans[:-1]:
            str_trans += coordinate[i][0] + ',' + coordinate[i][1] + ';'
        str_trans += coordinate[-1][0] + ',' + coordinate[-1][1]

        # 增加计数值
        k_trans += max_trans
        count += 1

        # http请求
        url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + str_trans + '&from=1&to=5&ak=' + akeys
        r = requests.get(url)

        # 提取转换结果
        response_dict = r.json()
        result_trans = response_dict['result']
        len_trans = len(result_trans)
        for i in np.arange(len_trans):
            longitude_trans.append(result_trans[i]['x'])
            latitude_trans.append(result_trans[i]['y'])

        print('----------------------Round ' + str(count) + ' Finished -------------------------')

    print(' Mission Description ')
    print('Numbers Of Dataset: ' + str(len_data))
    print('Numbers Of Iterations: ' + str(count))

    # 转换结果写入文件
    data['LONGITUDE'] = longitude_trans
    data['LATITUDE'] = latitude_trans
    data.to_csv('cleaned_data/0a0aaa2c5802f17d89ac93dc57633b76.csv', index=False)

    # 程序运行时间
    timestamp_end = time.time()
    time_spend = timestamp_end - timestamp_start
    print('Time Consumption: ' + str(time_spend) + ' s')

    print('---------------- Mission Completed ---------------------')

# 基于密度的聚类
def dj_cluster():
    # Neighbor半径
    eps = 2
    # 最少Neighbor数量
    min_pts = 50

    # 加载数据
    def load_data(link, username, password, database):
        # 打开数据库连接
        db = pymysql.connect(link, username, password, database)

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT trace_id,LONGITUDE,LATITUDE FROM 0a0aaa2c5802f17d89ac93dc57633b76")

        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()

        return data

    data = list(load_data('localhost', 'root', 'yzy950624', 'trace'))

    for i in range(len(data)):
        data[i] = list(data[i])

    # unprocessed_data包含未处理的点
    unprocessed_data = data.copy()
    # processed_data中保存经过density-join后，已生成的cluster
    processed_data = []
    # 噪声点
    noise_data = []

    # 计算两点间的真实距离
    def real_distance_Compute(point1, point2):
        if point1[1] == point2[1] and point1[2] == point2[2]:
            dist = 0

        else:
            # 角度转换为弧度
            long1 = (math.pi / 180) * float(point1[1])
            lan1 = (math.pi / 180) * float(point1[2])
            long2 = (math.pi / 180) * float(point2[1])
            lan2 = (math.pi / 180) * float(point2[2])
            # 地球半径
            earth_r = 6371
            # 计算公式
            dist = math.acos(
                math.sin(lan1) * math.sin(lan2) + math.cos(lan1) * math.cos(lan2) * math.cos(long2 - long1)) * earth_r

        return dist

    # 计算density-based neighborhood
    def Compute_Neighbor(point):

        neighbor = []
        for item in data:
            # 判断两点间的距离
            if real_distance_Compute(point, item) <= eps:
                neighbor.append(item)
        # 如果neighbor数量小于min_pts，返回空值
        if len(neighbor) < min_pts:
            neighbor = []

        return neighbor

    # 进行density-join
    def den_Join(point, neighbor):
        # density-join后的新cluster
        new_cluster = []
        # 如果processed_data不为空
        if len(processed_data):
            # 对processed_data中的每个cluster，判断其是否包含neighbor中的某个点
            for index, cluster in enumerate(processed_data):
                for item in neighbor:
                    # 如果存在，那么将原cluster合并到新的cluster中，并删除原cluster
                    if item in cluster:
                        new_cluster += cluster
                        del processed_data[index]
                        break

        # 将neighbor和point也合并到新的cluster中
        new_cluster += neighbor
        new_cluster.append(point)
        # 将新的cluster添加到processed_data
        processed_data.append(new_cluster)

    round = 1
    # 循环处理数据集中的每个元素直至未处理数据为空
    while len(unprocessed_data):

        print('round: {}'.format(round))
        round += 1

        point = unprocessed_data.pop()
        # 计算density-based neighborhood
        neighbor = Compute_Neighbor(point)
        # 若返回值不为空，进行density-join
        if len(neighbor):

            den_Join(point, neighbor)
            # 移除处理过的点
            for item in neighbor:
                if item in unprocessed_data:
                    unprocessed_data.remove(item)
        # 若返回值neighbor为空，则判断该点为噪声点
        else:
            noise_data.append(point)
            # 是否应该把噪声点从数据集中移除？
            data.remove(point)

    print('nums of clusters:{}'.format(len(processed_data)))
    print('nums of noise:{}'.format(len(noise_data)))

    # 更新聚类结果到数据库
    def update_database(link, username, password, database):

        db = pymysql.connect(link, username, password, database)
        cursor = db.cursor()

        for i in range(len(processed_data)):
            for item in processed_data[i]:
                # SQL 更新语句
                sql = 'UPDATE 0a0aaa2c5802f17d89ac93dc57633b76 SET cluster = {} WHERE trace_id = {}'.format(i + 1,
                                                                                                            item[0])
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    # 发生错误时回滚
                    db.rollback()

        db.close()

    update_database('localhost', 'root', 'yzy950624', 'trace')