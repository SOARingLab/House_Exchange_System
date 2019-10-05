from UserProfile.models import trace
import requests
from cluster_method.source.mysql_connect import save_profile
from data_analysis.profile_Extract import extract_Profile
import json

# 对POI查询结果进行解析并保存
def Memo_profile(POIs, home_coordinate, work_coordinate, other_clusters):

    # User Profile
    profile = {}

    # 暂时先取id=1的测试用户
    User_id = trace.objects.get(id=1).user_id
    profile['user_id'] = json.dumps(User_id)

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

    # 提取家庭和工作所在地,并以json格式存储在数据库中
    if 'result' in response_dict_home:
        home_place = response_dict_home['result']['formatted_address']
        profile['home_coordinate'] = json.dumps(home_coordinate)
        profile['home_location'] = json.dumps(home_place)
    if 'result' in response_dict_work:
        work_place = response_dict_work['result']['formatted_address']
        profile['work_coordinate'] = json.dumps(work_coordinate)
        profile['work_location'] = json.dumps(work_place)

    # 提取其它常去地点
    others_frequent = []
    for other_co in other_clusters:
        url = 'http://api.map.baidu.com/geocoder/v2/?location=' + other_co[1] + ',' + other_co[0] + \
                   '&output=json&pois=0&latest_admin=1&ak=' + akeys
        r = requests.get(url)
        response_dict = r.json()
        if 'result' in response_dict:
            place = response_dict['result']['formatted_address']
            others_frequent.append([other_co, place])

    # 提取POIs
    POI_labels_db = [['food_nums', 'food_detail'], ['hotel_nums', 'hotel_detail'], ['shopping_nums', 'shopping_detail'],
                    ['tourism_nums', 'tourism_detail'], ['entertainment_nums', 'entertainment_detail'],
                    ['sport_nums', 'sport_detail'], ['education_nums', 'education_detail'], ['medical_nums', 'medical_detail'],
                    ['transportation_nums', 'transportation_detail'], ['financial_nums', 'financial_detail'],
                    ['company_nums', 'company_detail'], ['natural_nums', 'natural_detail']]

    POI_labels = list(POIs.keys())

    # 将POI信息映射到相应的数据库字段
    for i in range(len(POI_labels)):
        profile[POI_labels_db[i][0]] = json.dumps(len(POIs[POI_labels[i]]))
        profile[POI_labels_db[i][1]] = json.dumps(POIs[POI_labels[i]])

    profile['other_places'] = json.dumps(others_frequent)

    # 在数据库中存储Profile
    #save_profile(profile)

    # 从数据库中读取profile
    # user_profile = extract_Profile(4, list(profile.keys()))


