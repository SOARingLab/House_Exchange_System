from source import disCompute


#计算density-based neighborhood
def Compute_Neighbor(point, original_data, eps):

	neighbor = []
	for item in original_data:
		#判断两点间的距离
		if disCompute.real_distance_Compute(point, item) <= eps:
			neighbor.append(item)
	neighbor.append(point)

	return neighbor