import pymysql


# 加载数据
def load_data(link, username, password, database):
    # 打开数据库连接
    db = pymysql.connect(link, username, password, database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT id,LONGITUDE,LATITUDE FROM UserProfile_trace")

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()

    db.close()

    return data


# 更新聚类结果到数据库
def update_database(link, username, password, database, processed_data):
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