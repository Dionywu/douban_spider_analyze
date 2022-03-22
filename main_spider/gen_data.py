from optparse import Values
from movie_spider import getData
from movie_spider import url

with open("./quotes.txt",'w',encoding="utf-8") as f:
    dic = getData(url)
    str = ""
    for value in dic.values():
        if(value[3]!="暂无介绍"):
            str += value[3]
    f.write(str)

with open("./type.txt",'w',encoding="utf-8") as f:
    dic = getData(url)
    str = ""
    for value in dic.values():
        if(value[6]!="信息不全"):
            str += value[6]
    f.write(str)
