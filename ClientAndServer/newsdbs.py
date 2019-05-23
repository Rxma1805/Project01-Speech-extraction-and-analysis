import pymysql

def getnews():
    """
    连接mysql数据库 执行sql语句
    :return: 返回所有content值
    """
    conn = pymysql.connect(
        host='cdb-q1mnsxjb.gz.tencentcdb.com',
        port=10102,
        user='root',
        passwd='A1@2019@me',
        db='news_chinese'
    )
    if conn:
        print('****** connection success ******')
    else:
        print('****** connection failed ******')
    cur = conn.cursor()

    print("*** proceeding the SQL query ***")
    cur.execute("select content  from sqlResult_1558435 ")

    news = []
    print("****  Loading data to news ****")
    for r in cur:
        news.append(r)
    if news:
        print('*** finish loading the content as news ***')
    else:
        print('*** failed in loading data  ***')
    cur.close()
    conn.close()
    print('*****  close the database ****')
    return news
