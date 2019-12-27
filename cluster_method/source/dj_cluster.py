from cluster_method.source import density_Join, mysql_connect, neighbor_com, timeFrequent
import datetime

def dj_cluster_algorithm():
    # Neighbor半径
    eps = 0.5
    # 最少Neighbor数量
    min_pts = 100

    # 重置数据表中的cluster字段
    mysql_connect.reset_database('localhost', 'root', 'wsnxdyj', 'user_trace')

    # 获取原始数据集
    data = list(mysql_connect.load_data('localhost', 'root', 'wsnxdyj', 'user_trace'))
    data = list(map(list, data))

    # unprocessed_data包含未处理的点
    d1 = datetime.datetime.now()
    unprocessed_data = data.copy()

    # processed_data中保存经过density-join后，已生成的cluster
    processed_data = []

    # 噪声点
    noise_data = []

    round = 1
    # 循环处理数据集中的每个元素直至未处理数据为空
    while unprocessed_data:

        # print('round: {}'.format(round))
        round += 1

        # 每次从unprocessed_data中取出一个未处理的点point
        point = unprocessed_data.pop()

        # 计算density-based neighborhood
        neighbor = neighbor_com.Compute_Neighbor(point, data, eps)

        # 计算N(p)是否满足要求
        if len(neighbor) < min_pts:
            # 如果不满足，则作为噪声点来处理
            noise_data.append(point)
            data.remove(point)
            continue

        # 进行density-joinable操作
        processed_data = density_Join.den_Join(neighbor, processed_data)

        # 移除处理过的点
        for item in neighbor:
            if item in unprocessed_data:
                unprocessed_data.remove(item)
    '''
    print('nums of clusters:{}'.format(len(processed_data)))
    print('nums of noise:{}'.format(len(noise_data)))
    '''
    d2 = datetime.datetime.now()
    interval = d2 - d1
    total_sec = interval.total_seconds()
    # 更新数据库
    # mysql_connect.update_cluster('localhost', 'root', 'wsnxdyj', 'user_trace', processed_data)

    return total_sec

if __name__ == "__main__":
    # execute only if run as a script
    dj_cluster_algorithm()