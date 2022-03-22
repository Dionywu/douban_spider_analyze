import urllib.request
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
from matplotlib.pyplot import title

url = "https://movie.douban.com/top250?start="

# re匹配
link_pattern = re.compile(r'<a href="(.*)">')
img_pattern = re.compile(r'src="(.*?)"',re.S)
title_pattern = re.compile(r'<span class="title">(.*?)</span>')
rank_pattern = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
ping_pattern = re.compile(r'<span>(.*)人评价</span>')
quote_pattern = re.compile(r'<span class="inq">(.*?)</span>')
content_pattern = re.compile(r'<p class="">(.*?)</p>',re.S)

index=["序号","名字","评分","评分人数","简介","导演","主演","类型","国家","日期"]


# 得到指定一个URL的网页内容
def askURL(url):
    head = {        # 模拟头
        "User-Agent":"Mozilla/5.0   (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
        "Cookie":r'bid=bR_jcKqwdjU; douban-fav-remind=1; __utmc=30149280; __gads=ID=40d9abd04054e27c-223ee917a3c6001f:T=1616333381:RT=1616333381:S=ALNI_MbBX_0loefyEcMPAqhArn9JyVS-lw; ll="108289"; __utmz=30149280.1647661059.2.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dbcl2="200010463:sDBHMUSLjp0"; ck=UVVc; push_noty_num=0; push_doumail_num=0; __utmv=30149280.20001; __utmc=223695111; __utmz=223695111.1647661251.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D5369A4C7B97111A610C40818DEC54FA8|402bc0d6021143ce8583ebc4a25fbf9e; _pk_ref.100001.4cf6=["","",1647704938,"https://www.douban.com/"]; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1102633225.1616333380.1647702557.1647704938.8; __utmb=30149280.0.10.1647704938; __utma=223695111.705964483.1647661251.1647702557.1647704938.7; __utmb=223695111.0.10.1647704938; _pk_id.100001.4cf6=3f251ba0e5f085c9.1647661251.6.1647706330.1647699647.'
    }
    req = urllib.request.Request(url=url,headers=head)
    res = urllib.request.urlopen(req)
    html = res.read().decode("utf-8")
    return html

def getUrlList(baseurl):    # 获取url列表（10页，就是10个url）
    urlists = [] 
    for i in range(10):
        urlists.append(baseurl + str(i*25))
    return urlists

def getData(baseurl):       # 返回一个字典，字典里存着电影的信息
    movie_dic = {} 
    urllist = getUrlList(baseurl)   # 获取所有url的列表
    xuhao = 0
    for ul in urllist:
        html = askURL(ul)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_ = "item"):
            xuhao += 1
            item = str(item) # 变为字符串，更好的进行匹配
            l = []

            # 链接可以不要
            # mov_link = re.findall(link_pattern,item)[0]
            # l.append(mov_link)
            # img_link = re.findall(img_pattern,item)[0]
            # l.append(img_link)

            title = re.findall(title_pattern,item)[0]
            l.append(title)
            rank = re.findall(rank_pattern,item)[0]
            l.append(rank)
            ping = re.findall(ping_pattern,item)[0]
            l.append(ping)
            quote = re.findall(quote_pattern,item)
            if len(quote) != 0:
                l.append(quote[0])
            else:
                l.append("暂无介绍")
            content = re.findall(content_pattern,item)[0]
            st = " ".join(content.split())
            li = st.strip().split(":")
            tu = ()
            try:       # 爬取内容可能会有一些对不上号
                director = li[1].split(" ")[1]
                actor = li[2].split(" ")[1]
                type = li[-1].split("/")[-1].split(" ")[1]
                contro = li[-1].split("/")[-2].split(" ")[1]
                year =  re.findall(r"\d\d\d\d",st)[0]
                tu = (director,actor,type,contro,year)
            except(IndexError):
                tu = ("信息不全","信息不全","信息不全","信息不全","信息不全")
            l.extend(tu)
            movie_dic[str(xuhao)] = l 
    return movie_dic

def getDF(dic):     # 
    d = pd.DataFrame(dic) 
    d = d.T
    d.reindex(columns=index)
    return d

if __name__ == '__main__':
    dic = getData(url)
    df = getDF(dic)
    df.to_csv("movie.csv",header=0,index=0)    