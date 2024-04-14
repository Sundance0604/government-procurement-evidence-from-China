Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import time
import os
import pandas as pd
import requests
from lxml import etree
import re
from tqdm import tqdm
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
folder_path= r'D:\myduty\goverment_purchase\data_respider\wangzhan'

def get_page(url,proxy_list,j):

    random_user_agent = ua.random
    header = {'User-Agent': random_user_agent}
    # 发起请求
    get_proxy=proxy_list[(j-1)%len(proxy_list)]
    proxies = {'http': 'http://' + get_proxy}
    session = requests.session()
    session.keep_alive = False  # 防止报错“Max retries exceeded with url”，关闭多余连接
    session.proxies.update(proxies)
    response = session.get(url, headers=header).text
    # response.text返回的是Unicode类型的数据，不能encoding为utf-8
    tree = etree.HTML(response)  # 实例化源码
    return tree,session
def read_page(tree,i):
    dict_temp = [None]*4
    info_ = tree.xpath(f'/html/body/div[5]/div[2]/div/div/div[1]/ul/li[{i}]/span/text()')[0]
    p_time, purchaser, agency = info_.split('|')
    p_time = p_time.strip()
    purchaser = purchaser.strip()
    agency = agency.strip()
    p_type = tree.xpath(f'/html/body/div[5]/div[2]/div/div/div[1]/ul/li[{i}]/span/strong[2]/text()')[0]
    contract_link = tree.xpath(f'/html/body/div[5]/div[2]/div/div/div[1]/ul/li[{i}]/a/@href')[0]
    dict_temp[0] = p_time
    dict_temp[1] = purchaser.split('：')[1].strip()
    dict_temp[2] = agency.split('：')[1].strip()
    dict_temp[3] = p_type.strip()

    return contract_link,dict_temp

def to_page(url, session):
    random_user_agent = ua.random
    header = {'User-Agent': random_user_agent}
    response_link = session.get(url=url, headers=header)
    response_link.encoding = response_link.apparent_encoding
    response_link = response_link.text
    tree = etree.HTML(response_link)
    paragraph_texts = tree.xpath('//*[@id="detail"]/div[2]//text()')
    info = '  '.join(text.strip() for text in paragraph_texts if text.strip())
    return info
def path_get():
    file_list = os.listdir(folder_path)
    file_path=[]
    for file in file_list:
        if file.endswith('.csv'):
            file_path.append(os .path.join(folder_path,file))
    return file_path
def main():

    
    proxy_list = [
    "183.153.124.89:4215",
    "183.153.124.75:4215",
    "125.125.226.230:4215",
    "125.125.234.103:4215",
    "122.230.35.226:4215",
    "125.125.143.50:4215",
    "122.230.59.141:4215",
    "125.125.233.250:4215",
    "125.125.140.38:4215",
    "115.208.164.78:4215",
    "125.125.141.57:4215",
    "122.230.34.184:4215",
    "122.230.61.128:4215",
    "125.125.237.144:4215",
    "125.125.231.214:4215",
    "115.207.253.136:4215",
    "125.125.235.224:4215",
    "183.142.205.45:4215",
    "125.125.239.130:4215",
    "122.239.155.60:4261",
    "115.208.164.89:4215",
    "122.230.59.130:4215",
    "183.153.123.103:4215",
    "183.142.200.36:4215",
    "49.89.87.111:4241",
    "122.239.130.153:4261",
    "125.125.129.100:4215",
    "125.125.226.208:4215",
    "183.153.123.98:4215",
    "114.239.2.173:4262",
    "49.70.95.251:4241",
    "122.239.150.137:4261",
    "183.142.204.98:4215",
    "122.230.34.174:4215",
    "114.239.2.71:4262",
    "122.230.43.153:4215",
    "49.70.95.203:4241",
    "183.153.107.36:4215",
    "125.125.129.214:4215"
    ]
    file_path=path_get()
    for file in file_path:
        filename= os.path.basename(file)
        filename=folder_path+"\\"+filename
        dict_temp=[]
        try:
            dict_temp = pd.read_csv(filename)
        except:
            dict_temp = pd.read_csv(filename, encoding='gbk')
        _type=dict_temp.iloc[2,2]
        dict_pages = []
        page=1
        for j in range(1, len(dict_temp)):
            j=page
            if j>=len(dict_temp):
                break
            error=False
            try:
...                 url_1 = dict_temp.iloc[j,0]
...                 # 获取网页信息
...                 tree_1, session = get_page(url_1, proxy_list, j)
...             except Exception as e:
...                 print(f"在获取网页信息时{str(e)}")
...                 error=True
...             
...             for i in range(1, 21):
...                 # 对公告进行爬取
...                 dict_list={}
...                 dict_list['网站页码']=url_1
...                 dict_list['所属类别']=dict_temp.iloc[j,1]
...                 dict_list['所属类型']=dict_temp.iloc[j,2]
...                 try:
...                     url_2, dict_ = read_page(tree_1, i)
...                     dict_list['发布时间'] = dict_[0]
...                     dict_list['采购人'] = dict_[1]
...                     dict_list['代理机构'] = dict_[2]
...                     dict_list['品目'] = dict_[3]
...                     dict_list['公告网站']= url_2
...                     
...                 except Exception as e:
...                     error=True
...                     continue
... 
...                 try:
...                     if url_2 is not None:
...                         full_text=""
...                         full_text = to_page(url_2, session)
...                         dict_list['全文内容']=full_text
...                 except Exception as e:
...                     print(f"在摘取全文时{str(e)}")
...                 dict_pages.append(dict_list)
...             if error:
...                 time.sleep(100)
...             print(f"{_type}第{j}页爬取完整"+str(error))
...             page=page+20
...         df = pd.DataFrame(dict_pages)
...         df.to_csv(f"{_type}网站.csv", index=False)
