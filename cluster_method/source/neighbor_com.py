from source import disCompute


#计算density-based neighborhood
def Compute_Neighbor(point, original_data, eps, min_pts):

	neighbor = []
	for item in original_data:
		#判断两点间的距离
		if disCompute.real_distance_Compute(point, item) <= eps:
			neighbor.append(item)
	#如果neighbor数量小于min_pts，返回空值
	if len(neighbor) < min_pts:
		neighbor = []

	return neighbor