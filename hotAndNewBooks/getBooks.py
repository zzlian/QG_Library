from QG_Library.dao import getHtml
from QG_Library.dao import switchUserAgent
from bs4 import BeautifulSoup
import re


def getNewBooks(url,userAgents,agent_index):
    """获取最新书籍"""

    #获取网页信息
    html = getHtml.getHtml(url,agent_index[0])
    #判断IP代理是否有用
    agentNumber = len(userAgents)
    k = 0
    while True:
        if k == agentNumber:
            break
        if html == "":
            agent_index = switchUserAgent.switchUserAgent(userAgents, agent_index)
            html = getHtml.getHtml(url, agent_index[0])
            k = k + 1
            print(str(666) + "...没用的代理")
        else:
            break
    soup = BeautifulSoup(html,"lxml")

    #提取网页中书的链接和书名
    contents = soup.find_all("ul", attrs={"class": "list-col list-col5 list-express slide-item"})[0]
    contents = contents.find_all("li", attrs={"class": ""})
    link_titles = []
    number = 0
    for content in contents:
        link_title = []
        content = re.findall(r'href(.*?)\>', str(content))
        link = re.findall(r'\=\"(.*?)\"', content[0])
        title = re.findall(r'title\=\"(.*?)\"', content[0])
        link_title.append(link[0])
        link_title.append(title[0])
        link_titles.append(link_title)
        number = number + 1
        if number == 10:
            break

    #由书的链接获取更详细的信息
    newBookMessages = []
    for link_title in link_titles:
        newBook = getBookMessage(link_title[0],link_title[1],userAgents,agent_index)
        newBookMessages.append(newBook)

    return newBookMessages


def getHotBooks(url,userAgents,agent_index):
    """获取热门书籍"""

    #获取网页中的信息
    html = getHtml.getHtml(url, agent_index[0])
    #判断IP代理是否有用
    agentNumber = len(userAgents)
    k = 0
    while True:
        if k == agentNumber:
            break
        if html == "":
            agent_index = switchUserAgent.switchUserAgent(userAgents, agent_index)
            html = getHtml.getHtml(url, agent_index[0])
            k = k + 1
            print(str(666) + "...没用的代理")
        else:
            break
    soup = BeautifulSoup(html, "lxml")

    # 提取网页中书的链接和书名
    contents = soup.find_all("ul", attrs={"class": "list-col list-col2 list-summary s"})[0]
    contents = contents.find_all("li", attrs={"class": ""})
    link_titles = []
    number = 0
    for content in contents:
        link_title = []
        content = re.findall(r'class\=\"\"\shref(.*?)a\>', str(content))
        link = re.findall(r'\=\"(.*?)\"\s', content[0])[0]
        title = re.findall(r'\"\>(.*?)\<', content[0])[0]
        link_title.append(link)
        link_title.append(title)
        link_titles.append(link_title)
        number = number + 1
        if number == 8:
            break

    # 由书的链接获取更详细的信息
    number = 0
    hotBookMessages = []
    for link_title in link_titles:
        hotBook = getBookMessage(link_title[0], link_title[1], userAgents, agent_index)
        hotBookMessages.append(hotBook)

    return hotBookMessages



def getBookMessage(bookLink,bookName,userAgents,agent_index):
    """从由链接获取到的详情网页中获取书的详细信息"""

    #保存书籍的相关信息
    bookMessage = {}

    #将传递过来的书名和链接保存
    bookMessage["书名"] = bookName
    bookMessage["豆瓣链接"] = bookLink
    bookMessage["类别"] = ""
    print(bookLink)

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
    if author == None:
        bookMessage["作者"] = ""

        #获取书的封面链接
    pictureLink=soup.find_all('div',attrs={"class":"","id":"mainpic"})
    if pictureLink:
        pictureLink = re.findall(r'href\=\"(.*?)\"', str(pictureLink[0]), re.S)
        if pictureLink:
            bookMessage["图片链接"] = pictureLink[0].strip()
    if pictureLink == None:
        bookMessage["图片链接"] = ""

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
    if introContext == None:
        bookMessage["内容简介"] = ""

    #获取书的评分
    rating=soup.find_all('strong',attrs={'class':'ll rating_num ','property':'v:average'})
    if rating:
        rating = re.findall("\>(.*?)\<\/", str(rating[0]), re.S)
        if rating:
            bookMessage["评分"] = rating[0].strip()
    if rating == None:
        bookMessage["评分"] = ""

    #获取书的ISBN码
    isbn=re.findall(r'\<span\sclass\=\"pl\"\>ISBN\:\<\/span\>(.*?)\<br',str(soup),re.S)
    if isbn:
        bookMessage["ISBN"] = isbn[0].strip()

    return bookMessage

