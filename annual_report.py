
import pandas as pd
import re
import os

def if_exist_four(text):

    exist_result=[None]*4
    if text:
        pattern = r"(√|)\s*适用"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            exist_result[0]="是"
        else:
            exist_result[0]="否"
    
        pattern = r"(√|)\s*不适用"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            exist_result[1]="是"
        else:
            exist_result[1]="否"
        
        pattern = r"不存在衍生品投资"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            exist_result[2]="是"
        else:
            exist_result[2]="否"
    
        pattern = r"不存在以投机为目的的衍生品投资"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            exist_result[3]="是"
        else:
            exist_result[3]="否"
    return exist_result

def if_exist_list(text):
    keyword_1=["远期","货币远期合约","货币远期","利率远期合约","利率远期","商品远期合约","商品远期"]

    keyword_2=['金属期货', '铜', '铝', '黄金', '白银','能源期货', '原油', '天然气',
            '农产品期货', '大豆', '小麦', '玉米', '棉花','股指期货', '沪深300', '上证50', '中证500',
            '国债期货', '5年期', '10年期', '2年期']

    keyword_3=['股票期权','指数期权','上证50','沪深300','商品期权','货币期权','美元','欧元','利率期权',
                '利率掉期期权','国债期权','ETF','上证50ETF期权','沪深300ETF期权','深证100ETF期权']

    keyword_4=['互换','利率互换','货币互换','商品互换','信用违约互换']


    exist_result=[None]*8
    i=0
    if text:
        for keyword in keyword_1,keyword_2,keyword_3,keyword_4:
            exist_word=""
            for word in keyword:
                if word in text:
                    exist_result[i]="是"
                    exist_word=exist_word+" "+word
            exist_result[i+1]=exist_word
            if exist_result[i+1] =="":
                exist_result[i]="否"
            i=i+2
           
    return exist_result
def path_get():
    folder_path= r'D:\myduty\goverment_purchase\2001~2022 年上市公司年报 txt 文件合集\上市公司年报txt'
    file_list = os.listdir(folder_path)
    file_path=[]
    for file in file_list:
        match1 = re.search(r'_([0-9]{4})_', file)
        if file.endswith('.txt') :
            if match1:
                file_year = int(match1.group(1))
                if file_year >= 2010:
                    file_path.append(os .path.join(folder_path,file))
    return file_path
    
def text_find(text):

    pattern = r"衍生品投资情况(.*?)募集资金使用情况"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        content_between = match.group(1).strip()
    else:
        content_between = None
    return content_between
    
def get_title(file):
    match1 = re.search(r'_([0-9]{4})_', file)
    match2 = re.search(r'(\d{6})',file)
    stock_code = match2.group(1)
    title=file.split('.')[0]
    file_year = int(match1.group(1))
    return file_year,stock_code,title

def contain_info():
    filename='D:\myduty\goverment_purchase\\包含衍生品的上市公司信息(1).xlsx'
    df = pd.read_excel(filename, usecols=[0, 2],dtype={0: str})
    return df
def main():
    file_path=path_get()
    company_info=contain_info()
    transfer=[]
    target_number=set(company_info.iloc[:,0])
    print(company_info)
    print(target_number)
    for file in file_path:
        
        filename= os.path.basename(file)
        year,stock_code,title=get_title(filename)
        if stock_code not in target_number:
            continue
        matching_indexes = company_info.index[company_info.iloc[:, 0] == stock_code].tolist()
        for match_index in matching_indexes:
            if year== int(company_info.iloc[match_index,1]):
                
                absolute_path = 'D:\myduty\goverment_purchase\\2001~2022 年上市公司年报 txt 文件合集\\上市公司年报txt\\' + filename
                with open(absolute_path, 'r', encoding='utf-8') as file:
                    text=""
                    text= file.read()
                dict_list={}
                dict_list['标题']=title
                dict_list['股票代码']=stock_code
                dict_list['年份']=year
        
                exist_list = if_exist_list(text)

        
                dict_list['是否包含第一列词频']=exist_list[0]
                dict_list['包含的第一列具体内容']=exist_list[1]
                dict_list['是否包含第二列词频']=exist_list[2]
                dict_list['包含的第二列具体内容']=exist_list[3]
                dict_list['是否包含第三列词频']=exist_list[4]
                dict_list['包含的第三列具体内容']=exist_list[5]
                dict_list['是否包含第四列词频']=exist_list[6]
                dict_list['包含的第四列具体内容']=exist_list[7]
                transfer.append(dict_list)
                print(match_index)
                break;
                
            
    df = pd.DataFrame(transfer)
    df.to_excel('年报.xlsx', index=False)
    print("success")
main()
        
        
        
