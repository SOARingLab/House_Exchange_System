from cluster_method.source.mysql_connect import load_profile

import json

# 从数据库中读取profile
def extract_Profile(ID, profile_items):
    # 以python字典的形式存储profile
    profile = {}

    data = load_profile(ID, profile_items)

    for idx, item in enumerate(profile_items):
        profile[item] = json.loads(data[idx])

    return profile