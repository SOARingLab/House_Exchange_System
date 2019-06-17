from cluster_method.source.mysql_connect import load_data_ana
from UserProfile.models import trace
from data_analysis.plotting import pie_plot
from data_analysis.timeDist_Cal import time_distribute_Cal
from data_analysis.activityDist_Cal import activity_distribute_Cal

# 使用初始时刻以及持续时间，推算数据点在各时间区间内的时间长度分布，并进行统计
def Analysis_clusters():

    # 聚类之后的类别数量
    cluster_count = trace.objects.values('cluster').distinct().count() - 1

    # 对每个类别进行可视化分析
    for i in range(1, cluster_count + 1):
        # 获取待处理数据，即每个聚类类别中数据点的start_time和duration
        data = list(load_data_ana('localhost', 'root', 'wsnxdyj', 'user_trace', i))
        data = list(map(list, data))

        # 计算每个类别中的时间区间分布和活动分布
        time_distribution = time_distribute_Cal(data)
        activity_distribution = activity_distribute_Cal(time_distribution)

        # 生成绘图所需的参数
        labels = list(activity_distribution.keys())
        sizes = list(activity_distribution.values())

        # 绘制饼状图
        pie_plot(labels, sizes)

# 调用Analysis_clusters方法进行可视化分析
Analysis_clusters()