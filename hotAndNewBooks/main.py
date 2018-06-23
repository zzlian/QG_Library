from QG_Library.dao import getUserAgents
from QG_Library.hotAndNewBooks import getBooks
from QG_Library.dao import storeBooks
from QG_Library.hotAndNewBooks import getThreeBooks

#IP代理池
userAgents = getUserAgents.getUserAgent()
agent_index = []
agent_index.append(userAgents[400])
agent_index.append(400)
agentNumber = len(userAgents)

#豆瓣链接
url = "https://book.douban.com/"

#新书、热门书籍、随机从数据库获取三本书
newBooks = getBooks.getNewBooks(url,userAgents,agent_index)
hotBooks = getBooks.getHotBooks(url,userAgents,agent_index)
randomBooks = getThreeBooks.getBooks()

books = []
for book in newBooks:
    books.append(book)
    print(book)
for book in hotBooks:
    books.append(book)
    print(book)
for book in randomBooks:
    books.append(book)
    print(book)

#存进数据库
storeBooks.storeNewAndHotBooks(books)
