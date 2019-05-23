
def TF(neighbor):
    # 总持续时间
    duration_sum = 0

    for item in neighbor:
        duration_sum += int(item[3])

    return duration_sum