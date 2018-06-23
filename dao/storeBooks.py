import pymysql


def storeAllBooks(books):
    """将所有类别的书籍存进数据库中"""

    # 链接数据库
    con = pymysql.connect(host='192.168.199.79', port=3306, user='root', passwd='password', db='qglibtest')
    con.set_charset('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    for book in books:
        try:
            sql = "insert into bookEX (ISBN,book_name,author,rating,picture,douban,cla,content,aboutwriter) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(book["ISBN"],book["书名"],book["作者"],book["评分"],book["图片链接"],book["豆瓣链接"],book["类别"],book["内容简介"],book["作者简介"]))
        except:
            pass

    cur.close()
    con.commit()
    con.close()


def storeNewAndHotBooks(books):
    """更新数据库中的新书和热书"""

    # 链接数据库
    con = pymysql.connect(host='192.168.199.79', port=3306, user='root', passwd='password', db='qglibtest')
    con.set_charset('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    #清空原本的新书和热书
    sql = "delete from books"
    cur.execute(sql)

    #添加新书和热书
    for book in books:
        try:
            sql = "insert into books (ISBN,book_name,author,rating,picture,douban,cla,content) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, (
            book["ISBN"], book["书名"], book["作者"], book["评分"], book["图片链接"], book["豆瓣链接"], book["类别"], book["内容简介"]))
        except:
            pass

    cur.close()
    con.commit()
    con.close()
