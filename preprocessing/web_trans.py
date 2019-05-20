import requests
import pandas as pd
import numpy as np
import time

#时间戳
timestamp_start = time.time()

data = pd.read_csv('cleaned_data/0a0aaa2c5802f17d89ac93dc57633b76.csv')

#经纬度坐标集
coordinate = data[['LONGITUDE','LATITUDE']].astype(str).values

#AK
akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'

#数据集长度
len_data = len(data)

#已转换数
k_trans = 0
#循环次数
count = 0

#转换后的经纬度
longitude_trans = []
latitude_trans = []

#单次请求的最大数量
max_trans = 100

#构建http请求转换原坐标为百度地图坐标
while k_trans <= len_data:
	#http请求的url字符串
	str_trans = ''
	#每批待转换的index
	index_trans = np.arange(0)

	#每次批量转换100个坐标
	#判断剩余未转换坐标数量
	if len_data - k_trans <= max_trans:
		index_trans = np.arange(k_trans,len_data)
	else:
		index_trans = np.arange(k_trans,k_trans + max_trans)
	
	#构建请求字符串
	for i in index_trans[:-1]:
		str_trans += coordinate[i][0] + ',' + coordinate[i][1] + ';'
	str_trans += coordinate[-1][0] + ',' + coordinate[-1][1]
	
	#增加计数值
	k_trans += max_trans
	count += 1

	#http请求
	url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + str_trans + '&from=1&to=5&ak=' + akeys
	r = requests.get(url)
	
	#提取转换结果
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

#转换结果写入文件
data['LONGITUDE'] = longitude_trans
data['LATITUDE'] = latitude_trans
data.to_csv('cleaned_data/0a0aaa2c5802f17d89ac93dc57633b76.csv',index = False)

#程序运行时间
timestamp_end = time.time()
time_spend = timestamp_end - timestamp_start
print('Time Consumption: ' + str(time_spend) + ' s')

print('---------------- Mission Completed ---------------------')

