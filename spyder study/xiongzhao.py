#-*- coding: utf-8 -*-
import requests
import re
import json
import threading
import pymongo
import random
import time
from matplotlib.font_manager import FontProperties 
import matplotlib
font = FontProperties(fname="/System/Library/Fonts/STHeiti Light.ttc", size=14) 
matplotlib.rcParams['font.sans-serif'] = ['Fangsong'] 
matplotlib.rcParams['font.family']='sans-serif'

#解决负号’-‘显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False

def find_producet_id(key_word):
    jd_url = 'https://search.jd.com/Search'
    product_ids = []
    for i in range(1,3):
        param = {'keyword':key_word,'enc':'utf-8','page':i}
        kv = {'user-agent': 'Mozilla/5.0'}
        try:
            response = requests.get(jd_url,params=param,headers = kv)
            #print(response.text)
        except:
            print('爬取失败')
        ids = re.findall('data-pid="(.*?)"',response.text,re.S)
        product_ids += ids
    return product_ids

def get_comment_message(product_id):
    
    url2 = 'https://item.jd.com/%s.html'%product_id
    kv = {'user-agent': 'Mozilla/5.0'}
    header = { 'user-agent': 'Mozilla/5.0','referer':'https://item.jd.com/%s.html'%product_id}
    response = requests.get(url2,headers=kv)
    comment_version = re.findall("commentVersion:'(.*?)'",response.text,re.S)
    print(comment_version)
    urls = ['https://sclub.jd.com/comment/productPageComments.action?'\
            'callback=fetchJSON_comment98vv{}&'\
            'productId={}'\
            '&score=0&sortType=5&'\
            'page={}'\
            '&pageSize=10&isShadowSku=0&fold=1'.format(comment_version[0],product_id,page) for page in range(1,11)] 
    for url in urls:
        response = requests.get(url,headers=header)
        html = response.text
        html = html.replace('fetchJSON_comment98vv%s('%comment_version[0], '').replace(');','')
        #print(html)
        #print(len(html))
        if len(html)>10:
            data = json.loads(html)
            comments = data['comments']
            t = threading.Thread(target=save_mongo,args=(comments,))
            t.start()
        time.sleep(2)
        
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = client.jd_url
product_db = db.product

def save_mongo(comments):
    for comment in comments:
        product_data = {}

        product_data['product_color'] = flush_data(comment['productColor'])

        product_data['product_size'] = flush_data(comment['productSize'])

        product_data['product_content'] = (comment['content'])

        product_data['create_time'] = (comment['creationTime'])

        result = product_db.insert(product_data)

        print(product_db)
#def flush_data(data):
def flush_data(data):
    if '1' in data:
        print('hhihi')
    if '肤' in data:
        return '肤色'
    if '黑' in data:
        return '黑色'
    if '紫' in data:
        return '紫色'
    if '粉' in data:
        return '粉色'
    if '蓝' in data:
        return '蓝色'
    if '白' in data:
        return '白色'
    if '灰' in data:
        return '灰色'
    if '槟' in data:
        return '槟色'
    if '琥' in data:
        return '琥色'
    if '红' in data:
        return '红色'
    if 'A' in data:
        return 'A'
    if 'B' in data:
        return 'B'
    if 'C' in data:
        return 'C'
    if 'D' in data:
        return 'D'
    if 'E' in data:
        return 'E'
    if 'F' in data:
        return 'F'


lock = threading.Lock()
def spider_jd(ids):
    while ids:
        lock.acquire()
        id = ids[0]
        del ids[0]
        lock.release()
        get_comment_message(id)
from pylab import *
if __name__ == "__main__":
    # product_ids = find_producet_id('胸罩')
    # for i in range(1,5):
    #     t = threading.Thread(target=spider_jd,args=(product_ids,))  
    #     t.start() 
    color_arr = [u'肤色',u'黑丝','紫色','粉色','蓝色','白色','灰色','香槟色','红色']
    color_num_arr = []
    for i in color_arr:
        num = product_db.count({'product_color':i})
        color_num_arr.append(num)
    colors= ['bisque','black','purple','pink','blue','white','gray','peru','red']
    plt.figure('hihi')
    patches,l_text,p_text = plt.pie(color_num_arr,labels=color_arr,colors=colors,labeldistance=1.1,
    autopct='%3.1f%%',shadow=False,startangle=90,pctdistance=0.6)
    for t in l_text:
        t.set_size(20)
        t.set_fontproperties(font)
    for t in p_text:
        t.set_size(10)
    plt.axis('equal')
    plt.title(u'颜色对比',fontproperties=font)
    plt.legend(prop=font)
    plt.show()
