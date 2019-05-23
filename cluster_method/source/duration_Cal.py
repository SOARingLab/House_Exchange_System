"""计算两个时间戳的间隔时间"""

def DurationCal(timeline1, timeline2):

    # timeline原格式：201806101009
    # 解析格式：2018/06/10/10:09
    time1 = timeline1[6:]
    time2 = timeline2[6:]
    item1, item2 = [], []
    item1.append(time1[:2])
    item2.append(time2[:2])
    item1.append(time1[2:4])
    item2.append(time2[2:4])
    item1.append(time1[4:])
    item2.append(time2[4:])

    res = (int(item2[0]) * 24 * 60 + int(item2[1]) * 60 + int(item2[2])) - (int(item1[0]) * 24 * 60 + int(item1[1]) * 60 + int(item1[2]))

    return res
