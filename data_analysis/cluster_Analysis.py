from cluster_method.source.mysql_connect import load_data_ana
from UserProfile.models import trace
from data_analysis.plotting import pie_plot, line_chart
from data_analysis.timeDist_Cal import time_distribute_Cal
from data_analysis.activityDist_Cal import activity_distribute_Cal
from django.db.models import Avg, Sum
from data_analysis.poi_Search import search_POI, search_Address
from data_analysis.profile_Generate import Memo_profile


# 使用初始时刻以及持续时间，推算数据点在各时间区间内的时间长度分布，并进行统计
def Analysis_clusters():

    # 聚类之后的类别数量
    cluster_count = trace.objects.values('cluster').distinct().count() - 1

    # 计算各聚类中心点坐标
    cluster_avg = []
    for i in range(cluster_count):
        avg_longitude = str(trace.objects.filter(cluster=i + 1).aggregate(Avg('longitude'))['longitude__avg'])
        avg_latitude = str(trace.objects.filter(cluster=i + 1).aggregate(Avg('latitude'))['latitude__avg'])
        cluster_avg.append([avg_longitude, avg_latitude])

    # 存储各类别的home_time和working_time
    home_candidate = []
    work_candidate = []

    # 保存所有类别中的时间区间分布
    cluster_data = []

    # 对每个类别进行可视化分析
    for i in range(1, cluster_count + 1):
        # 获取待处理数据，即每个聚类类别中数据点的start_time和duration
        data = list(load_data_ana('localhost', 'root', 'wsnxdyj', 'user_trace', i))
        data = list(map(list, data))

        # 每个类别中的时间区间分布
        time_distribution = time_distribute_Cal(data)

        cluster_data.append([list(time_distribution.keys()), list(time_distribution.values())])

        # 每个类别中的时间活动分布
        activity_distribution = activity_distribute_Cal(time_distribution)

        # 将home_time和working_time单独存储
        duration_sum = trace.objects.filter(cluster=i).aggregate(Sum('duration'))['duration__sum']
        home_candidate.append(activity_distribution['HomeTime'] / duration_sum)
        work_candidate.append(activity_distribution['WorkTime'] / duration_sum)

        # 生成绘图所需的参数
        labels = list(activity_distribution.keys())

        #labels = ['在家时间','工作时间','午饭时间','晚饭时间','夜生活时间']
        sizes = list(activity_distribution.values())

        # 绘制饼状图
        #pie_plot(labels, sizes)

    # 绘制折线图
    #line_chart(cluster_data)


    # 筛选出home_time最长的cluster作为家庭住址所在地
    home_cluster = home_candidate.index(max(home_candidate)) + 1
    work_cluster = work_candidate.index(max(work_candidate)) + 1

    # home/working place 坐标
    home_coordinate = cluster_avg[home_cluster - 1]
    work_coordinate = cluster_avg[work_cluster - 1]

    print(search_Address(home_coordinate))

    # 除home&working place 之外的其余常去地点
    cluster_avg.remove(home_coordinate)
    cluster_avg.remove(work_coordinate)

    # 搜索居住地周边的POI分布
    #home_POIs = search_POI(home_coordinate)
    # 对Profile进行持久化存储
    #Memo_profile(home_POIs, home_coordinate, work_coordinate, cluster_avg)

# 调用Analysis_clusters方法进行可视化分析
Analysis_clusters()


