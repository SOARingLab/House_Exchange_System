from source import density_Join, mysql_connect, neighbor_com

#Neighbor半径 0.5
eps = 2
#最少Neighbor数量 120
min_pts = 50

# 获取原始数据集
data = list(mysql_connect.load_data('localhost', 'root', 'wsnxdyj', 'user_trace'))
data = list(map(list, data))

#unprocessed_data包含未处理的点
unprocessed_data = data.copy()

#processed_data中保存经过density-join后，已生成的cluster
processed_data = []

#噪声点
noise_data = []

round = 1
#循环处理数据集中的每个元素直至未处理数据为空
while unprocessed_data:

	print('round: {}'.format(round))
	round += 1

    #每次从unprocessed_data中取出一个未处理的点point
	point = unprocessed_data.pop()

	#计算density-based neighborhood
	neighbor = neighbor_com.Compute_Neighbor(point, data, eps, min_pts)

	#若返回值不为空，进行density-join
	if neighbor:
		neighbor.append(point)
		processed_data = density_Join.den_Join(neighbor, processed_data)

		#移除处理过的点
		for item in neighbor:
			if item in unprocessed_data:
				unprocessed_data.remove(item)

	#若返回值neighbor为空，则判断该点为噪声点
	else:
		noise_data.append(point)
		#是否应该把噪声点从数据集中移除？
		data.remove(point)

print('nums of clusters:{}'.format(len(processed_data)))
print('nums of noise:{}'.format(len(noise_data)))

#更新数据库
mysql_connect.update_database('localhost', 'root', 'wsnxdyj', 'user_trace', processed_data)