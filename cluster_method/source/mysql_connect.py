import pymysql


# 加载数据
def load_data(link, username, password, database):
    # 打开数据库连接
    db = pymysql.connect(link, username, password, database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT id,LONGITUDE,LATITUDE,DURATION FROM UserProfile_trace")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()

    db.close()

    return data

# 加载数据，用于分析每类数据的时间分布
def load_data_ana(link, username, password, database, cluster):
    # 打开数据库连接
    db = pymysql.connect(link, username, password, database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT start_time,duration FROM UserProfile_trace WHERE cluster = " + str(cluster))

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()

    db.close()

    return data


# 更新T-DJ-Cluster聚类结果到数据库
def update_cluster(link, username, password, database, processed_data):
    db = pymysql.connect(link, username, password, database)
    cursor = db.cursor()

    for i in range(len(processed_data)):
        for item in processed_data[i]:
            # SQL 更新语句
            sql = 'UPDATE UserProfile_trace SET cluster = {} WHERE id = {}'.format(i + 1, item[0])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()

    db.close()

# 更新KMeans聚类结果
def update_cluster_kmeans(link, username, password, database, result):
    db = pymysql.connect('localhost', 'root', 'wsnxdyj', 'user_trace')
    cursor = db.cursor()

    for i in range(len(result)):
        sql = 'UPDATE UserProfile_trace SET cluster = {} WHERE id = {}'.format(result[i], i + 1)

        try:
            cursor.execute(sql)
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

    db.close()

# 重置数据库中的cluster字段
def reset_database(link, username, password, database):
    db = pymysql.connect(link, username, password, database)
    cursor = db.cursor()
    sql = 'UPDATE UserProfile_trace SET cluster = 0'

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()

# 存储Profile结果
def save_profile(profile):
    link = 'localhost'
    username = 'root'
    password = 'wsnxdyj'
    database = 'user_trace'
    db = pymysql.connect(link, username, password, database)
    columns = ''
    for column in profile.keys():
        columns += column + ','
    columns = '(' + columns[:-1] + ')'
    values = str(tuple(profile.values()))
    cursor = db.cursor()
    sql = 'INSERT INTO UserProfile_profile' + columns + ' VALUES ' + values
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()

def load_profile(ID, profile_items):
    link = 'localhost'
    username = 'root'
    password = 'wsnxdyj'
    database = 'user_trace'
    db = pymysql.connect(link, username, password, database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    items = ''
    for item in profile_items:
        items += item + ','
    items = items[:-1]

    sql = "SELECT " + items + " FROM UserProfile_profile WHERE id=" + str(ID)
    cursor.execute(sql)
    data = cursor.fetchone()

    db.close()

    return data
