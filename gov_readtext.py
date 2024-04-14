Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import pandas as pd
import re
import os

folder_path= r'D:\myduty\goverment_purchase\data_respider\wangzhan'


def path_get():
    
    file_list = os.listdir(folder_path)
    file_path = []
    for file in file_list:
        if file.endswith('.csv'):
            file_path.append(os .path.join(folder_path,file))
    return file_path

def base_info(text):
    
    if not isinstance(text,str):
        text = str(text)
    info = [None] * 4  
    answer = [None] * 4  
    info[0] = re.compile(r'(?:项 目 编 号|项目编号|招标文件编号)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    info[1] = re.compile(r'(?:项目名称|项 目 名 称)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    info[2] = re.compile(r'(?:金额（人民币）|预算金额|金额)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    info[3] = re.compile(r'(?:供应商名称)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    
    for i in range(0,4):
        matches = None
        #显然，你想要获取所有匹配项的第一个
        matches = info[i].findall(text)
        if i==0:
            if matches:
                if len(matches)>1:
                    answer[i]= re.sub(r'^.*：', '', matches[1])  # 将第一个匹配项（是一个字符串）中“：”之前的内容删除
                else:
                    answer[i] = re.sub(r'^.*：', '', matches[0])
        else:
            if matches:
                answer[i] = re.sub(r'^.*：', '', matches[0])  # 将第一个匹配项（是一个字符串）中“：”之前的内容删除
    return answer


def keyword_check(text,keyword_return):
    if not isinstance(text,str):
        text = str(text)
    
    keyword_1=['落实政府采购政策','中小企业','中小微企业','小微企业','非专门面向中小企业','不专门面向中小企业','专门面向中小企业'
            ,'不专门面向中小微企业','专门面向中小微企业','非专门面向中小微企业']#8
    keyword_2=['联合体','接受联合体','不接受联合体','接受联合体：是','接受联合体：否','接受联合体投标：否','接受联合体投标：是']#7
    keyword_3=['分包','接受分包','不接受分包','接受分包：是','接受分包：否']#5
    
    for keyword in keyword_1, keyword_2, keyword_3:
        for word in keyword:
            if word in text:
                keyword_return[word] = "是"
            else:
                keyword_return[word] = "否"
                
    if keyword_return['专门面向中小企业']=="是":
        if keyword_return['非专门面向中小企业']=="否"  and keyword_return['不专门面向中小企业']=="否":
            keyword_return["是否专门面向中小（微）企业"]="是"
        else:
            keyword_return["是否专门面向中小（微）企业"]="否"
    elif keyword_return['专门面向中小微企业']=="是":
        if keyword_return['非专门面向中小微企业']=="否"  and keyword_return['不专门面向中小微企业']=="否":
            keyword_return["是否专门面向中小（微）企业"]="是"
        else:
            keyword_return["是否专门面向中小（微）企业"]="否"
    else:
        keyword_return["是否专门面向中小（微）企业"]="否"
        
    if keyword_return['接受联合体']=="是":
        if keyword_return['不接受联合体']=="否" and  keyword_return['接受联合体：否']=="否":
            keyword_return['是否接受联合体']="是"
        else:
            keyword_return['是否接受联合体']= "否"
    else:
        keyword_return['是否接受联合体']= "否"
        
    if keyword_return['接受分包'] == "是":
        if keyword_return['不接受分包']=="否" and  keyword_return['接受分包：否']=="否":
            keyword_return['是否接受分包']="是"
...         else:
...             keyword_return['是否接受分包']="否"
...     else:
...         keyword_return['是否接受分包']="否"
... def main():
...     file_path=path_get()
...     for file in file_path:
...         filename= os.path.basename(file)
...         filename1 = filename.split('.')[0] + "_分析.csv" 
...         filename=folder_path+"\\"+filename
...         dict_temp=[]
...         try:
...             dict_temp = pd.read_csv(filename)
...         except:
...             dict_temp = pd.read_csv(filename, encoding='gbk')
...         transfer=[]
...         rate = 0
...         _type = dict_temp.iloc[2, 2]
...         for i in range(1,len(dict_temp)):
...             dict_list={}
...             original = dict_temp.iloc[i].to_dict()
...             answer=base_info(dict_temp.iloc[i, 8])
...             dict_list['项目编号']=answer[0]
...             dict_list['项目名称']=answer[1]
...             dict_list['金额']=answer[2]
...             if dict_temp.iloc[i, 2] == "中标公告" or dict_temp.iloc[i, 2] == "成交公告":
...                 dict_list['供应商名称'] = answer[3]
...             else:
...                 pass
...             if _type!="中标公告" and _type!="成交公告" and _type != "更正公告" and _type != "终止公告":
...                 keyword_check(dict_temp.iloc[i, 8], dict_list)
...         
...             original.update(dict_list)
...             transfer.append(original)
...         df = pd.DataFrame(transfer)
...         df.to_csv(filename1, index=False)
...         print("success")
