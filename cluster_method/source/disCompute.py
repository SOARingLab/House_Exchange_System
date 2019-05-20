import math

#计算两点间的真实距离
def real_distance_Compute(point1,point2):
	if point1[1] == point2[1] and point1[2] == point2[2]:
		dist = 0

	else:
		#角度转换为弧度
		long1 = (math.pi/180)*float(point1[1])
		lan1 = (math.pi/180)*float(point1[2])
		long2 = (math.pi/180)*float(point2[1])
		lan2 = (math.pi/180)*float(point2[2])
		#地球半径
		earth_r = 6371.393
		#计算公式
		dist = math.acos(math.sin(lan1) * math.sin(lan2) + math.cos(lan1) * math.cos(lan2) * math.cos(long2 - long1)) * earth_r

	return dist