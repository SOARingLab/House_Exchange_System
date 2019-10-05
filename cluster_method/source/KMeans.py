import pandas as pd
from sklearn.cluster import KMeans
import pymysql
from cluster_method.source import mysql_connect

#重置数据表中的cluster字段
mysql_connect.reset_database('localhost', 'root', 'wsnxdyj', 'user_trace')

# 获取原始数据集
data = list(mysql_connect.load_data('localhost', 'root', 'wsnxdyj', 'user_trace'))
data = list(map(list, data))

# 数据预处理，将原始数据转换成DataFrame格式
data = pd.DataFrame(data)
data.columns = ['id', 'LONGITUDE', 'LATITUDE', 'DURATION']
del data['id']
del data['DURATION']

# 运行KMeans算法
kmeans = KMeans(n_clusters=3).fit_predict(data)
data['result'] = kmeans

# 更新数据库
mysql_connect.update_cluster_kmeans('localhost','root','wsnxdyj','user_trace', kmeans)