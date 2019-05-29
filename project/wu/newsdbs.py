import pymysql

class db():

    def connect(self):
        """
        连接mysql数据库 执行sql语句
        :return: 返回所有content值
        """
        self.conn = pymysql.connect(
            host='cdb-q1mnsxjb.gz.tencentcdb.com',
            port=10102,
            user='root',
            passwd='A1@2019@me',
            db='news_chinese'
        )
        if self.conn:
            print('****** connection success ******')
        else:
            print('****** connection failed ******')

    def do_execute(self,sql,id=None):
        cur = self.conn.cursor()

        print("*** proceeding the SQL query ***")
        # if id:
        cur.execute(sql,(id))
        # else:
        #     cur.execute(sql)

        result = cur.fetchall()


        cur.close()
        print('*****  close the database ****')
        return result

    def get_counts(self):
        return self.do_execute('select count(*)  from sqlResult_1558435')[0][0]



    def get_content(self,id):
        return self.do_execute('select content from sqlResult_1558435 where id = %s',id=id)


    def close(self):
        conn.close()


if __name__ == '__main__':

    db = db()
    db.connect()
    count = db.get_counts()

    import random
    id = random.randint(0,int(count))
    print(id)

    data = db.get_content(id)
    print(data)

