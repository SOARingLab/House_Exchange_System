from cluster_method.source import dj_cluster, T_dj_cluster, KMeans

# 计算算法运行十次的平均时间
def alg_time_Cal():
    # 记录算法运行时间
    res = []
    for i in range(10):
        res.append(T_dj_cluster.T_dj_cluster_algorithm())
    print(res)
    print(sum(res)/10)

if __name__ == "__main__":
    # execute only if run as a script
    alg_time_Cal()