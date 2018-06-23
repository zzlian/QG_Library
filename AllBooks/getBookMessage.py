from bs4 import BeautifulSoup
from QG_Library.dao import getHtml
from QG_Library.dao import switchUserAgent
import re


def switchPage(url,doubanUrl,userAgents,agent_index):
    """判断下一页是否还有该类小说，若有，返回下一页的url"""

    agentNumber = len(userAgents)
    html = getHtml.getHtml(url,agent_index[0])
    k = 0
    while True:
        if k == agentNumber:
            break
        if html == "":
            agent_index = switchUserAgent.switchUserAgent(userAgents,agent_index)
            html = getHtml.getHtml(url, agent_index[0])
            k = k + 1
            print(str(666)+"...没用的代理")
        else:
            break

    soup = BeautifulSoup(html,"lxml")

    #先粗略获取下一页的链接，逐步精确
    newPage = re.findall(r'thispage(.*?)\<\/a\>',str(soup),re.S)
    if newPage:
        newPage = re.findall(r'href="(.*?)">',newPage[0],re.S)

    if not newPage or not re.findall(r'start(.*)T',newPage[0]):
        return ""

    #若存在下一页的链接，获取下一页的信息，判断下一页是否存在书
    else:
        newPage = doubanUrl+newPage[0]
        html = getHtml.getHtml(newPage,agent_index[0])
        k = 0
        #判断当前代理是否IP是否有用，没用更换下一个IP
        while True:
            if k == agentNumber:
                break
            if html == "":
                agent_index = switchUserAgent.switchUserAgent(userAgents, agent_index)
                html = getHtml.getHtml(newPage, agent_index[0])
                k = k + 1
                print(str(666)+"...没用的代理")
            else:
                break

        soup = BeautifulSoup(html,"lxml")
        hasBook = re.findall(r'thispage(.*)\<\/a\>',str(soup),re.S)
        if hasBook:
            return newPage
        else:
            return ""


def getMessage(html,tag,userAgents,agent_index):
    """由获取的网页信息获取需要的书籍信息"""

    soup = BeautifulSoup(html, 'lxml')
    messages = []

    # 由html得到每本书的信息片段
    contents = soup.find_all('h2', attrs={'class': ''})

    # 由书的信息片段得到相应的书名和链接
    for content in contents:
        message = {}
        s = re.findall(r'title\=\"(.*?)\"\>', str(content))
        if s:
            message['书名'] = s[0].strip()
        else:
            continue

        s = re.findall(r'href\=\"(.*?)\"', str(content))
        if s:
            message['链接'] = s[0].strip()
        else:
            continue

        messages.append(message)

    #由获取到的书的链接获取该书的详情网页
    bookMessages = []
    for message in messages:
        bookMessage = getBookMessage(message["链接"],message["书名"],tag,userAgents,agent_index)
        if bookMessage == "":
            continue
        bookMessages.append(bookMessage)


    return bookMessages


def getBookMessage(bookLink,bookName,tag,userAgents,agent_index):
    """从由链接获取到的详情网页中获取书的详细信息"""

    #保存书籍的相关信息
    bookMessage = {}
    #记录信息是否缺失，缺失则丢弃
    flag = 1

    #将传递过来的书名和链接保存
    bookMessage["书名"] = bookName
    bookMessage["豆瓣链接"] = bookLink
    bookMessage["类别"]=tag

    html = getHtml.getHtml(bookLink,agent_index[0])
    agentNumber = len(userAgents)
    k = 0
    while True:
        if k == agentNumber:
            break
        if html == "":
            agent_index = switchUserAgent.switchUserAgent(userAgents, agent_index)
            html = getHtml.getHtml(bookLink, agent_index[0])
            k = k + 1
            print(str(666) + "...没用的代理")
        else:
            break

    soup = BeautifulSoup(html, 'lxml')

    #获取书的作者
    author = soup.find_all("div",attrs={"class":"","id":"info"})
    if author:
        author = re.findall(r'href\=\"(.*?)a\>', str(author[0]), re.S)
        if author:
            author = re.findall(r'\>(.*?)\<',author[0],re.S)
            if author:
                author_0 = author[0].split("\n");
                author = ""
                for a in author_0:
                    author = author + a.strip()
                bookMessage["作者"] = author
            else :
                bookMessage["作者"] = ""
                flag = 0
        else:
            bookMessage["作者"] = ""
            flag = 0
    else :
         bookMessage["作者"] = ""
         flag = 0

    #获取书的封面链接
    pictureLink=soup.find_all('div',attrs={"class":"","id":"mainpic"})
    if pictureLink:
        pictureLink = re.findall(r'href\=\"(.*?)\"', str(pictureLink[0]), re.S)
        if pictureLink:
            bookMessage["图片链接"] = pictureLink[0].strip()
        else:
            bookMessage["图片链接"] =''
            flag = 0
    else:
        bookMessage["图片链接"] =''
        flag = 0


    #获取书的作者简介
    introContext=soup.find_all("div",attrs={"class":"indent "})
    if introContext:
        introContext = re.findall(r'\<p\>(.*?)\<\/div\>', str(introContext[0]),re.S)
        if introContext:
            context = ""
            contexts = introContext[0].split(r"</p> <p>")
            for c in contexts:
                context = context + c
            authorIntro = re.findall(r'(.*?)\<\/p\>', context)[0]
            authorIntro = re.sub(r'\s*',"",authorIntro)
            bookMessage["作者简介"] = authorIntro.strip()
        else:
            bookMessage["作者简介"] = ''
            flag = 0

    else:
        bookMessage["作者简介"] =''
        flag = 0


    #获取书的内容简介
    introContext=soup.find_all("div",attrs={"class":"related_info"})
    if introContext:
        introContext = re.findall(r'\<p\>(.*?)\<\/div\>', str(introContext[0]), re.S)
        if introContext:
            context = ""
            contexts = introContext[0].split(r"</p> <p>")
            for c in contexts:
                context = context + c
            contextIntro = re.findall(r'(.*?)\<\/p\>', context)[0]
            contextIntro = re.sub(r'\s*',"",contextIntro)
            bookMessage["内容简介"] = contextIntro
        else:
            bookMessage["内容简介"] = ''
            flag = 0

    else:
        bookMessage["内容简介"] =''
        flag = 0

    #获取书的评分
    rating=soup.find_all('strong',attrs={'class':'ll rating_num ','property':'v:average'})
    if rating:
        rating = re.findall("\>(.*?)\<\/", str(rating[0]), re.S)
        if rating:
            bookMessage["评分"] = rating[0].strip()
        else:
            bookMessage["评分"] = ''
            flag = 0
    else:
        bookMessage["评分"] =''
        flag = 0

    #获取书的ISBN码
    isbn=re.findall(r'\<span\sclass\=\"pl\"\>ISBN\:\<\/span\>(.*?)\<br',str(soup),re.S)
    if isbn:
        bookMessage["ISBN"] = isbn[0].strip()
    else:
        bookMessage["ISBN"] =''
        flag = 0

    if flag == 1:
        return bookMessage
    else :
        return ""






