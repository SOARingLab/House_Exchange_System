# 数据可视化
import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise
def pie_plot(labels, sizes):

    # 将最大的部分突出显示
    explode = [0.0 for _ in range(len(labels))]

    max_num, max_idx = 0, 0

    for idx, num in enumerate(sizes):
        if num > max_num:
            max_num = num
            max_idx = idx

    explode[max_idx] = 0.1

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()