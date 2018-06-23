from bs4 import BeautifulSoup
from QG_Library.dao import getHtml
from QG_Library.dao import switchUserAgent
import re


def getTagUrls(html,url,tags):
    """获取所有分类的链接，同时保存书的六大类的tag"""

    soup = BeautifulSoup(html, 'lxml')

    # 将html里每个标签的信息片段截取出来
    labels_0 = soup.find_all('td')
    labels = []

    # 由标签的信息片段得到相应的标签
    for tag in labels_0:
        t = re.findall(r'\"\>(.*?)\<\/a\>', str(tag))
        t = re.findall(r"\'(.*?)\'", str(t))
        if t[0] == '一刻' or t[0] == '豆瓣' or t[0] == '豆瓣摄影':
            continue
        labels.append(t[0].strip())

    # 标签加豆瓣读书的链接得到每个书类的链接
    urls = []
    for t in labels:
        url_tag=[]
        url_0 = url + t
        url_tag.append(url_0)
        for tag in tags.keys():
            if t in tags[tag]:
                url_tag.append(tag)
                break
        urls.append(url_tag)
    return urls


def getTags(url,userAgents,agent_index):
    """得到书的六大类的标签，同时将六大类的标签和多个小分类的标签对应起来"""
    agentNumber = len(userAgents)
    html = getHtml.getHtml(url,agent_index[0])
    k = 0
    while True:
        if k == agentNumber:
            break
        if html == "":
            agent_index = switchUserAgent.switchUserAgent(userAgents,agent_index)
            html = getHtml.getHtml(url, agent_index[0])
            k = k+1
            print(str(666) + "...没用的代理")
        else:
            break

    soup = BeautifulSoup(html,"lxml")


    #粗略地将信息根据六大类分为六个小块
    content = re.findall(r'style\=\"padding\-top\:10px(.*?)\<\/tbody\>',str(soup),re.S)

    tags = {}
    #在各个小块中得到大类标签，同时和多个小分类标签对应起来
    for c in content:
        #得到大类标签
        tag = re.findall(r'\"\>(.*?)\s\·',c,re.S)[0]

        #按小分类标签将信息分块
        labels_0 = re.findall(r'href(.*?)a\>\<b\>',c,re.S)

        #将大类标签和小分类标签对应起来
        labels = []
        for lab in labels_0:
            label = re.findall(r'\"\>(.*?)\<\/',lab,re.S)
            if label:
                labels.append(label[0])


        tags[tag] = labels

    return tags