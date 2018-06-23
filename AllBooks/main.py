from QG_Library.dao import getHtml
from QG_Library.AllBooks import getTagUrls
from QG_Library.AllBooks import getBookMessage
from QG_Library.dao import storeBooks
from QG_Library.dao import getUserAgents
from QG_Library.dao import switchUserAgent

#IP代理池
userAgents = getUserAgents.getUserAgent()
agent_index = []
agent_index.append(userAgents[200])
agent_index.append(200)
agentNumber = len(userAgents)

#初始链接
url = "https://book.douban.com/tag/"
html = getHtml.getHtml(url,agent_index[0])
#判断当前的代理IP是否可用，在不可用的情况下更换下一个代理IP
k=0
while True:
    if k == agentNumber:
        break
    if html == "":
        agent_index = switchUserAgent.switchUserAgent(userAgents,agent_index)
        html = getHtml.getHtml(url, agent_index[0])
        k = k+1
        print(str(666)+"...没用的代理")
    else:
        break


tags = getTagUrls.getTags(url,userAgents,agent_index)
urls = getTagUrls.getTagUrls(html,url,tags)

url = "https://book.douban.com"

#获取每一个链接得到的信息
#bookMessages=[]
pageNumber = 1
j = 0
for ur in urls:
    tag = ur[1]
    ur = ur[0]


    while True:
        html = getHtml.getHtml(ur,agent_index[0])

        #判断当前的代理IP是否可用，在不可用的情况下更换下一个代理IP
        k=0
        while True:
            if k == agentNumber:
                break
            if html == "" or pageNumber %50 == 0:
                pageNumber = pageNumber + 1
                agent_index = switchUserAgent.switchUserAgent(userAgents,agent_index)
                html = getHtml.getHtml(ur, agent_index[0])
                k = k+1
                print(str(666)+"...没用的代理")
            else:
                break

        #获取每一个网页中的书籍的信息
        print("现在书的小标签为： "+tag+"...链接为："+ur)
        bookMessage = getBookMessage.getMessage(html,tag,userAgents,agent_index)

        #将书存进数据库
        storeBooks.storeAllBooks(bookMessage)

        #for book in bookMessage:
            #if book not in bookMessages:
                #bookMessages.append(book)

        #进行换页
        pageNumber = pageNumber + 1
        ur = getBookMessage.switchPage(ur,url,userAgents,agent_index)
        if ur == "":
            break

