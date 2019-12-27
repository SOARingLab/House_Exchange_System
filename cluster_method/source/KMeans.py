import pandas as pd
import datetime
from sklearn.cluster import KMeans
import pymysql
from cluster_method.source import mysql_connect

def KMeans_algorithm():
	# 重置数据表中的cluster字段
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
	d1 = datetime.datetime.now()
	kmeans = KMeans(n_clusters=3).fit_predict(data)
	d2 = datetime.datetime.now()
	interval = d2 - d1
	total_sec = interval.total_seconds()
	data['result'] = kmeans
	# 更新数据库
	# mysql_connect.update_cluster_kmeans('localhost', 'root', 'wsnxdyj', 'user_trace', kmeans)

	return total_sec



if __name__ == "__main__":
	# execute only if run as a script
	KMeans_algorithm()