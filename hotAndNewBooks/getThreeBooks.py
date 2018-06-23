import random
import pymysql

def getBooks():
    """随机从数据库中获取三本书"""

    # 链接数据库
    con = pymysql.connect(host='192.168.199.79', port=3306, user='root', passwd='password', db='qglibtest')
    con.set_charset('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    #从数据库中随机选取三本书
    books = []
    for i in range(0,3):
        book = {}
        id = int(20000 * random.random())
        sql = "select * from bookEX where ID=" + str(id)
        cur.execute(sql)
        r = cur.fetchone()
        book["ISBN"] = r[1]
        book["书名"] = r[2]
        book["作者"] = r[3]
        book["评分"] = r[4]
        book["图片链接"] = r[5]
        book["豆瓣链接"] = r[6]
        book["类别"] = r[7]
        book["内容简介"] = r[8]
        books.append(book)

    return books