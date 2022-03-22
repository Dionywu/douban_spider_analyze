# 制作词云

from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sqlite3


img = Image.open("../img/tree.jpg")
img_np = np.array(img)
font_path = "/System/Library/fonts/PingFang.ttc"
quote_path = "../quotes.txt"
type_path = "../type.txt"

def genTX(path):      # 读取文件中的内容，用jieba进行分词，返回对应词频字典
    with open(path,'r',encoding='utf-8') as f:
        contents = f.read()
    content_list = jieba.lcut(contents)
    dic = {}
    for item in content_list:
        if len(item)>=2:
            if item in dic.keys():
                dic[item] += 1
            else:
                dic[item] = 1 
    # print(dic)
    # content_str = ""
    # for key in dic.keys():
    #     content_str = content_str +  key + " "
    return dic

if __name__ == '__main__':

    wc = WordCloud(
    font_path = font_path,
    mask = img_np,
    background_color = "white",
    )

    freq_dict = genTX(type_path)
    wc.generate_from_frequencies(freq_dict)     # 根据词频构造次云
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig("../word_type.jpg",dpi = 400)