import requests

# 搜素给定坐标点的POI分布
def search_POI(coordinate):

    # POI候选类别
    POIs = ['美食', '酒店', '购物', '旅游景点', '休闲娱乐', '运动健身', '教育培训', '医疗', '交通设施', '金融', '公司企业',
            '自然地物']

    akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'

    # 对每类POI的结果进行存储
    cluster_POI = {}

    # 针对每个候选的POI类别
    for POI in POIs:
        # 调用百度地图API
        url = 'http://api.map.baidu.com/place/v2/search?query=' + POI + '&location=' + coordinate[1] + ',' \
              + coordinate[0] + '&radius=1000&output=json&ak=' + akeys

        r = requests.get(url)

        # 处理返回值
        response_dict = r.json()

        # 检查返回的结果字段是否为空
        if 'results' in response_dict:
            result_trans = response_dict['results']

            # 存储查找到的该类POI的名称和地址
            loc = []

            for item in result_trans:
                loc.append([item['name'], item['address']])

            # 对每类POI的结果进行存储
            cluster_POI[POI] = loc

        else:
            cluster_POI[POI] = 'None'

    return cluster_POI

# 返回用户居住地所在位置
def search_Address(coordinate):
    akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'
    url = 'http://api.map.baidu.com/reverse_geocoding/v3/?ak=' + akeys + '&output=json&' \
          'coordtype=bd09ll&location=' + coordinate[1] + ',' + coordinate[0]

    r = requests.get(url)
    response_dict = r.json()

    if 'result' in response_dict:
        return response_dict['results']['formatted_address']