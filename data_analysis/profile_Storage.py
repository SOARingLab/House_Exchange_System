from UserProfile.models import trace
import requests

# 对POI查询结果进行解析并保存
def Memo_profile(POIs, home_coordinate, work_coordinate, other_clusters):

    # 暂时先取id=1的测试用户
    User_id = trace.objects.get(id=1).user_id

    # 调用百度地图API
    akeys = 'joLVEFit1SFGg6g1cgHzDZ1Dr9Up9D9H'

    url_home = 'http://api.map.baidu.com/geocoder/v2/?location=' + home_coordinate[1] + ','+ home_coordinate[0] +\
          '&output=json&pois=0&latest_admin=1&ak=' + akeys
    url_work = 'http://api.map.baidu.com/geocoder/v2/?location=' + work_coordinate[1] + ',' + work_coordinate[0] + \
               '&output=json&pois=0&latest_admin=1&ak=' + akeys

    r_home = requests.get(url_home)
    r_work = requests.get(url_work)

    # 处理返回值
    response_dict_home = r_home.json()
    response_dict_work = r_work.json()

    # 提取家庭和工作所在地
    if 'result' in response_dict_home:
        home_place = response_dict_home['results']['formatted_address']
    if 'result' in response_dict_work:
        work_place = response_dict_work['results']['formatted_address']


