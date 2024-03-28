Python 3.11.8 (tags/v3.11.8:db85d51, Feb  6 2024, 22:03:32) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import time
import pandas as pd
import requests
from lxml import etree
import re
from tqdm import tqdm
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

proxy_list = [
    "113.133.30.12:4231",
    "114.224.128.202:4246",
    "122.239.156.121:4248",
    "219.145.13.58:4229",
    "122.236.19.57:4246",
    "125.125.226.207:4215",
    "1.84.252.212:4243",
    "58.45.108.153:4247",
    "223.156.87.159:4234",
    "114.217.68.191:4283"
]
ua = UserAgent()
def contains_chinese(s):
    for char in s:
        if '\u4e00' <= char <= '\u9fa5':
            return True
    return False

def page_url(page):
    start_dict = {'2016年': '2016%3A01%3A01', '2017年': '2017%3A01%3A01', '2018年': '2018%3A01%3A01',
                  '2019年': '2019%3A01%3A01', '2020年': '2020%3A01%3A01', '2021年': '2021%3A01%3A01',
                  '2022年': '2022%3A01%3A01', '2023年': '2023%3A01%3A01'
                  }  # 选择起始时间
    end_dict = {'2016年': '2016%3A12%3A31', '2017年': '2017%3A12%3A31', '2018年': '2018%3A12%3A31',
                '2019年': '2019%3A12%3A31', '2020年': '2020%3A12%3A31', '2021年': '2021%3A12%3A31',
                '2022年': '2022%3A12%3A31', '2023年': '2023%3A12%3A31'}  # 选择截止时间
    bid_sort = {'所有类别': 0, '中央公告': 1, '地方公告': 2}  # 选择类别
    pinmu_dict = {'所有品目': 0, '货物类': 1, '工程类': 2, '服务类': 3}  # 选择品目
    bid_type = {'所有类型': 0, '中标公告': 7, '成交公告': 11}  # 选择类型


        # 尝试发一个请求
    url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=' + str(page) + \
          '&bidSort=' + str(bid_sort["地方公告"]) + '&buyerName=&projectId=&pinMu=' + str(pinmu_dict['工程类']) \
          + '&bidType=' + str(bid_type["中标公告"]) + '&dbselect=bidx&kw=&start_time=' \
          + start_dict["2022年"] + '&end_time=' + end_dict["2022年"] \
          + '&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
    return url

def page_info(page):
    
    # 生成随机的User-Agent
    random_user_agent = ua.random
    header = {'User-Agent': random_user_agent}
    print(header)
    # 发起请求
    get_proxy=proxy_list[(page-1)%len(proxy_list)]
    print(get_proxy)
    proxies = {'http': 'http://' + get_proxy}
    session = requests.session()
    session.keep_alive = False  # 防止报错“Max retries exceeded with url”，关闭多余连接
    session.proxies.update(proxies)
    response = session.get(url=page_url(page), headers=header).text
    # response.text返回的是Unicode类型的数据，不能encoding为utf-8
    tree = etree.HTML(response)  # 实例化源码
    # 准备好拼接url的参数
    
    
    try:
        page_info_elements = tree.xpath('/html/body/div[5]/div[2]/div/div/div[1]/p/script//text()')
        page_info = page_info_elements[0]
        # 其他代码继续执行
         # page_info是<class 'lxml.etree._ElementUnicodeResult'>类型的数据，需要转换为字符串类型才能进行正则匹配
        output = ''
        for i in page_info:
            output += str(i)  # 将page_info转换成str格式

        # 匹配size值的正则表达式模式
        pattern = r'size:\s*(\d+)'
    
        # 匹配出对应的size值，size的值就是总页码数
        match = re.search(pattern, output)
        page_size = match.group(1)  # 得到总页码数
    
        x = page  # 记录页码
        m = int(page_size)
        p = 1  # 记录信息条数
        process_ = m - x + 1
        # pbar = tqdm(total=process_)
        pbar_page = tqdm(total=1)
        pbar_num = tqdm(total=20)
        # 开始计时
        start = time.time()
        # 创建日志
        log_root = []
    
        # 初始化列表
        dict_list=[]
        for i in range(1, 21):
            random_delay = random.uniform(0, 1)
            time.sleep(random_delay)  
            
            try:
                dict_temp = {}
                info_ = tree.xpath(f'/html/body/div[5]/div[2]/div/div/div[1]/ul/li[{i}]/span/text()')[0]
                p_time, purchaser, agency = info_.split('|')
                p_time = p_time.strip()
                purchaser = purchaser.strip()
                agency = agency.strip()
                p_type = tree.xpath(f'/html/body/div[5]/div[2]/div/div/div[1]/ul/li[{i}]/span/strong[2]/text()')[0]
                contract_link = tree.xpath(f'/html/body/div[5]/div[2]/div/div/div[1]/ul/li[{i}]/a/@href')[0]
                dict_temp['发布时间'] = p_time
                dict_temp['采购人'] = purchaser.split('：')[1].strip()
                dict_temp['代理机构'] = agency.split('：')[1].strip()
                dict_temp['所属类型'] = p_type.strip()
                dict_temp["网站位置"]=f'{page},{i}'  
                
                url_link = contract_link
                # link_list.append(url_link)
                response_link = session.get(url=url_link, headers=header)
                response_link.encoding = response_link.apparent_encoding  # 让response_link正确解码，以防出现乱码
                response_link = response_link.text
                time.sleep(0.2)
                tree_1 = etree.HTML(response_link)
                try:
                #对项目编号处理
                    try:
                        paragraph_texts = tree_1.xpath('//*[@id="detail"]//text()')
                        code_info = 'END'.join(text.strip() for text in paragraph_texts if text.strip())
                        pattern_code = re.compile(r'(?:项目编号|项 目 编 号|招标文件编号|采购计划编号|项目号)：(.*?)(?=END|$)', re.DOTALL)
                        matches = pattern_code.findall(code_info)
        
                        if len(matches) >= 2:
                            project_code_with_colon = matches[1].strip()
                            project_code = re.sub(r'^.*：', '', project_code_with_colon)
                            if project_code.strip():
                                dict_temp['项目编号'] = project_code
                            else:
                                raise Exception()
                        elif len(matches)==1: 
                            pattern_code = re.compile(r'(?:项目编号|项 目 编 号|招标文件编号|采购计划编号|项目号)[:：\s]*END\s*([^\s"END]+)', re.DOTALL)
                            matches = pattern_code.findall(code_info)
                            project_code_with_colon = matches[0].strip()
                            dict_temp['项目编号'] = project_code_with_colon.strip()
                            
                        else:
                            raise Exception()
                    except Exception as e:
                        try:
                            pattern_code = re.compile(r'(?:项目编号|项 目 编 号|招标文件编号|采购计划编号|项目号)：(.*?)(?=END|$)', re.DOTALL)
                            matches = pattern_code.findall(code_info)
                            project_code_with_colon = matches[0].strip()
                            project_code = re.sub(r'^.*：', '', project_code_with_colon)
                            if project_code.isspace():
                                dict_temp['项目编号'] = project_code
                            else:
                                raise Exception()
                        except Exception as e:
                            try:
                                pattern_code = re.compile(r'(?:项目编号|项 目 编 号|招标文件编号|采购计划编号|项目号)[:：\s]*END\s*([^\s"END]+)', re.DOTALL)
                                matches = pattern_code.findall(code_info)
                                project_code_with_colon = matches[0].strip()
                                dict_temp['项目编号'] = project_code_with_colon.strip()
                            except Exception as e:
                                print(f'目前的爬取{p}条信息中，项目编号问题为{e}')
                            
                 #对项目名称处理       
                    try:
                        pattern_code = re.compile(r'(?:项目名称|采购项目名称)[:：\s]*END\s*([^\s"END]+)', re.DOTALL)
                        matches = re.findall(pattern_code,code_info)
                        match_code = re.search(pattern_code, code_info)
                        project_code_with_colon = match_code.group()
                        project_code = re.sub(r'^.*END\s*', '', project_code_with_colon)
                        dict_temp['项目名称'] = project_code
                        
                    except Exception as e:
                        try:
                            pattern_code = re.compile(r'(?:项目名称|采购项目名称)：(.*?)(?=END|$)', re.DOTALL)
                            matches = re.findall(pattern_code,code_info)
                            match_code = re.search(pattern_code, code_info)
                            project_code_with_colon = match_code.group()
                            project_code = re.sub(r'^.*：', '', project_code_with_colon)
                            dict_temp['项目名称'] = project_code
                            
                        except Exception as e:
                            print(f'目前的爬取{p}条信息中，项目名称问题为{e}')
                            
                    #对供应商名称进行处理
                    try:
                        pattern_supplier_name = re.compile(r'(?:供应商名称|采购代理机构全称|中标供应商名称|采购代理机构名称|成交供应商名称|中标单位)：(.*?)(?=END|$)', re.DOTALL)
                        matches_supplier_name = pattern_supplier_name.findall(code_info)
                        supplier_names = ', '.join(name.strip() for name in matches_supplier_name)
                        if contains_chinese(supplier_names):
                            dict_temp['供应商名称'] = supplier_names
                        else:
                            raise Exception
                    except Exception as e: 
                        try:
                            pattern_supplier_name = re.compile(r'(?:供应商名称|采购代理机构全称|中标供应商名称|采购代理机构名称|成交供应商名称|中标单位)[:：\s]*END\s*([^\s"END]+)', re.DOTALL)
                            matches_supplier_name = pattern_supplier_name.findall(code_info)
                            supplier_names = ', '.join(name.strip().replace('END', '') for name in matches_supplier_name)
                            dict_temp['供应商名称'] = supplier_names
                        except Exception as e:    
                            print(f'目前的爬取{p}条信息中，问题为{e}')
                    #对中标金额进行处理
                    try:
                        pattern_amount = re.compile(r'(?:中标金额|总中标金额|中标（成交）金额|成交金额|中标总金额|中标金额（人民币）)：(.*?)(?=END|$)', re.DOTALL)
                        matches_amount = pattern_amount.findall(code_info)
                        amounts = ', '.join(match.strip() for match in matches_amount)
                        if bool(re.search('\d', amounts)):
                            dict_temp['中标金额'] = amounts
                        else:
                            raise Exception
                        
                    except Exception as e: 
                        try:
                            pattern_amount = re.compile(r'(?:中标金额|总中标金额|中标（成交）金额|成交金额|中标总金额|中标金额（人民币）)[:：\s]*END\s*([^\s"END]+)', re.DOTALL)
                            matches_amount = pattern_amount.findall(code_info)
                            amounts = ', '.join(match.strip().replace('END', '') for match in matches_amount)
                            dict_temp['中标金额'] = amounts
                        except Exception as e:    
                            print(f'目前的爬取{p}条信息中，问题为{e}')
   
                
                except Exception as e:
                    print(f'目前的爬取{p}条信息中，问题为{e}')
                    random_delay = random.uniform(0, 1)
                    time.sleep(random_delay)  
                   
                            
                           
                if dict_temp:
                    dict_list.append(dict_temp)
...                
...                 pbar_num.update(1)
...               
...                 # 设置一个随机延时
...                 
...             except Exception as e:                      
...                 print(f'循环中，目前已爬取{p}条信息，问题为{e}')
...             p += 1
...                 
...         return dict_list
...     except Exception as e:   
...         print(f'第{page}页未找到页码信息，可能是页面结构发生变化，跳过处理。')
... 
... def main():
...     hello=input("输入任何数字确保程序开始，注意filename和起始值,ip是否可用？")
...    
...    
...     filename="GONGCHENG_22_789S1000.xlsx"
...     for page in range(1,2000):
...         dict_list=[]
...         dict_list=page_info(page)
...         if page==1 or page==1000:                
...             if page==1000:
...                 filename=filename1  
...             
...             df = pd.DataFrame(dict_list)
...             df.to_excel(filename, index=False)
...             print(f'数据已保存至 {filename}第{page}页爬取成功')
...             
...         else:
...                     # 读取原有Excel文件
...             existing_data = pd.read_excel(filename)
... 
...                     # 创建新的DataFrame
...             new_data = pd.DataFrame(dict_list)
... 
...             # 读取原有Excel文件134
...             existing_data = pd.read_excel(filename, sheet_name='Sheet1')
... 
...             # 在现有DataFrame的末尾追加新数据
            merged_data = pd.concat([existing_data, new_data], ignore_index=True)

            # 将合并后的DataFrame写入Excel文件，使用openpyxl引擎
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                merged_data.to_excel(writer, index=False, sheet_name='Sheet1')

            print(f'数据已追加至 {filename}第{page}页爬取成功')
main()
