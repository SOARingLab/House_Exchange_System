# 进行density-join操作
def den_Join(neighbor, processed_data):
    # density-join后的新cluster
    new_cluster = []
    new_processed_data = []

    if processed_data:
        # 对processed_data中的每个cluster，判断其是否包含neighbor中的某个点
        for index, cluster in enumerate(processed_data):

            # 设置flag，标记当前处理的cluster是否与neighbor是join-able的
            joinable = False

            for item in neighbor:
                # 如果存在，那么将原cluster合并到new_cluster中
                if item in cluster:
                    new_cluster += cluster
                    joinable = True
                    break

            # 如果没有join-able，那么将当前cluster不做任何变动，加入到new_processed_data中
            if not joinable:
                new_processed_data.append(cluster)

    # 将neighbor和point也合并到新的cluster中
    new_cluster += neighbor
    # 将新的cluster添加到new_processed_data
    new_processed_data.append(new_cluster)

    return new_processed_data