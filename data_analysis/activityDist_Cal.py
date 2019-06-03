
# 完成从时间区间分布到活动分布的映射
def activity_distribute_Cal(time_distribution):

    # 从时间区间分布到用户日常活动分布的映射规则

    """
    Mapping rules from time_distribution to activity_distribution:

    home time: 22:00pm to 08:00am
    working time: 08:00 to 12:00 and 14:00 to 17:00
    lunch time: 12:00 to 14:00
    dinner time: 17:00 to 19:00
    night time: 19:00 to 22:00
    """

    # 存储该类别数据中用户活动的分布情况
    activity_distribution = {'home_time': 0, 'working_time': 0, 'lunch_time': 0, 'dinner_time': 0, 'night_time': 0}

    # 根据映射规则进行分类统计
    for i in range (0, 24):
        # keys in time_distribution
        str_key = str(i) + '-' + str(i + 1)

        # working-time
        if i in range(8, 12) or i in range(14, 17):
            activity_distribution['working_time'] += time_distribution[str_key]

        # home-time
        elif i in range(22, 24) or i in range(0, 8):
            activity_distribution['home_time'] += time_distribution[str_key]

        # lunch-time
        elif i in range(12, 14):
            activity_distribution['lunch_time'] += time_distribution[str_key]

        # dinner-time
        elif i in range(17, 19):
            activity_distribution['dinner_time'] += time_distribution[str_key]

        # night-time
        elif i in range(19, 22):
            activity_distribution['night_time'] += time_distribution[str_key]

    return activity_distribution