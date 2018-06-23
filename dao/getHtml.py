import requests


def getHtml(url, userAgent):
    """由链接获取网页的信息"""
    try:
        session = requests.session()
        proxie = {
            'http': 'http://'+userAgent
        }

        r = session.get(url, proxies=proxie)
        r.raise_for_status()
        r.encoding = ('utf8')
        return r.text
    except:
        return ""


