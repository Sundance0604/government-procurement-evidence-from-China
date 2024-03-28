Python 3.11.8 (tags/v3.11.8:db85d51, Feb  6 2024, 22:03:32) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import pandas as pd
import re
import os

keywords=[["银行网络", "金融监管", "审慎监管", "巴塞尔", "系统性风险", "金融危机"],
          ["banking network", "banking regulation", "prudential regulation", "Basel", "systemic risk", "financial crisis"]]

filepath= r'D:\myduty\system_risk\article_2019_2023\世界经济学，期刊论文清单'

#year,sheet_name,language(0 china),title,JR
index=[[2019,1,1,4,1],[2019,2,0,3,1],[2020,0,0,5,2],[2020,1,1,6,2],
      [2021,0,1,3,2],[2021,1,0,2,1],[2022,0,1,3,2],[2022,1,1,2,1],
      [2022,2,0,4,1]
     ]


def keyword(text,keywords):
    if text:
        contained_keywords = [keyword for keyword in keywords if keyword in text]
        return ','.join(contained_keywords)
    else:
        return None

def main():
    write_out="监督.xlsx"
...     transfer=[]
...     for i in range(0,9):
...         year=index[i][0]
...         page=index[i][1]
...         language=index[i][2]
...         title_position=index[i][3]
...         JR=index[i][4]
...         
...         filename=filepath+"，"+str(year)+".xlsx"
...         print(filename)
...         
...         dict_temp=pd.read_excel(filename,sheet_name=page)
...         
...         names=dict_temp.iloc[1, JR]
...         for j in range(1,len(dict_temp)):
...             
...             dict_list={}
...             
...             try:
...                 
...                 if dict_temp.iloc[j, JR] is not None:
...                     names=dict_temp.iloc[j, JR]
...                 title_keyword=keyword(dict_temp.iloc[j, title_position],keywords[language])
...                 if title_keyword:
...                     
...                     dict_list['期刊名']=names
...                     dict_list['文章名']=dict_temp.iloc[j, title_position]
...                     dict_list['关键词']=title_keyword
...                     dict_list['年份']=str(year)
...                     transfer.append(dict_list)
...                     
...             except Exception as e:
...                 print(e)
...            
...             
...     df = pd.DataFrame(transfer)
...     df.to_excel(write_out, index=False)
...     print(write_out)
