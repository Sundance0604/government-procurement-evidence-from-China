Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import pandas as pd
import re
import os

folder_path= r'D:\myduty\goverment_purchase\data_respider\qiquan'
def path_get():
    
    file_list = os.listdir(folder_path)
    file_path=[]
    for file in file_list:
        if file.endswith('.csv'):
            file_path.append(os .path.join(folder_path,file))
    return file_path

def read_combine():
   
    file_path=path_get()
    file_type=['公开招标','询价公告','竞争性谈判','单一来源','邀请公告', '更正公告','终止公告','中标公告', '成交公告','竞争性磋商']
   
    for _type in file_type:
        transfer=[]
        print(_type)
        for file in file_path:
            filename= os.path.basename(file)
            if _type in filename:
                filename1=folder_path+"\\"+filename
                try:
                    data = pd.read_csv(filename1)
                except:
                    data = pd.read_csv(file, encoding='gbk')
                transfer.append(data)
        if transfer:
            df=pd.concat(transfer, ignore_index=True)
            df.to_csv(f"{_type}.csv", index=False)
            print("1")

def check_spider():
   
    file_path=path_get()
    for file in file_path:
        filename= os.path.basename(file)
        filename=folder_path+"\\"+filename
        dict_temp=[]
        try:
            dict_temp = pd.read_csv(filename)
        except:
            dict_temp = pd.read_csv(filename, encoding='gbk')
        respider_one=[]
        respider_all=[]
...         _type=dict_temp.iloc[2,2]
...         page_delet=[]
...         for j in range(1,len(dict_temp)):
...             if j>=len(dict_temp):
...                 break
...             line={}
...             if pd.isnull(dict_temp.iloc[j,8]):
...                 if pd.isnull(dict_temp.iloc[j,7])==False:
...                     line['网站页码']=dict_temp.iloc[j,0]
...                     line['所属类别']=dict_temp.iloc[j,1]
...                     line['所属类型']=dict_temp.iloc[j,2]
...                     line['发布时间']=dict_temp.iloc[j,3]
...                     line['采购人']=dict_temp.iloc[j,4]
...                     line['代理机构']=dict_temp.iloc[j,5]
...                     line['品目']=dict_temp.iloc[j,6]
...                     line['公告网站']=dict_temp.iloc[j,7]
...                     respider_one.append(line)
...                     page_delet.append(j)
...             if pd.isnull(dict_temp.iloc[j,7]):
...                 line['网站页码']=dict_temp.iloc[j,0]
...                 line['所属类别']=dict_temp.iloc[j,1]
...                 line['所属类型']=dict_temp.iloc[j,2]
...                 respider_all.append(line)
...                 for i in range(0,20):
...                     if j+i<len(dict_temp):
...                         page_delet.append(j+i)
...                     else:
...                         break
...                 j=j+19
...         
...         df_1=pd.DataFrame(respider_one)
...         df_2=pd.DataFrame(respider_all)
...         df_3=dict_temp.drop(page_delet)
...         df_1.to_csv(f"{_type}公告重爬.csv",index=False)
...         df_2.to_csv(f"{_type}网页重爬.csv",index=False)
...         df_3.to_csv(f"{_type}好.csv",index=False)
...         print(1)
...     print(2)
... 
