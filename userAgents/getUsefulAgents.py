# -*- coding:utf8 -*-
from urllib import request
import urllib
import socket
import os


def getUsefulAgents():
    """获取有用的IP代理"""

    #清空指定文件的内容，更新数据
    os.remove(r"C:\Users\lenovo\Desktop\super_agent.txt")

    socket.setdefaulttimeout(3)

    inf = open(r"C:\Users\lenovo\Desktop\agent_0.txt")  # 这里打开刚才存ip的文件
    lines = inf.readlines()
    proxys = []
    for i in range(0, len(lines)):
        proxy_host = "http://" + lines[i]
        proxy_temp = {"http": proxy_host}
        proxys.append(proxy_temp)

    # 用这个网页去验证，遇到不可用ip会抛异常
    url = "https://book.douban.com/tag/"
    # 将可用ip写入指定文件中
    ouf = open(r"C:\Users\lenovo\Desktop\super_agent.txt", "a+")

    for proxy in proxys:
        try:
            proxy_support = urllib.request.ProxyHandler(proxy)
            opener = urllib.request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent', 'Test_Proxy_Python3.5_maminyao')]
            urllib.request.install_opener(opener)
            response = urllib.request.urlopen(url)
            valid_ip = proxy['http'][7:]
            print("value" + valid_ip)
            ouf.write(valid_ip)
        except Exception as e:
            print(proxy)
            print(e)
            continue

