import pandas as pd
import re
import os

keywords=[["银行网络", "金融监管", "审慎监管", "巴塞尔", "系统性风险", "金融危机"],[
    "banking network", "banking regulation", "prudential regulation", "Basel", "systemic risk", "financial crisis"]]

filepath= r'D:\myduty\system_risk\article_2019_2023\世界经济学，期刊论文清单'



def keyword(text,keywords):
    if text:
        contained_keywords = [keyword for keyword in keywords if keyword in text]
        return ','.join(contained_keywords)
    else:
        return None

def main():
    
    year=input("print filename year")
    page=input("input sheet_name")
    title_position=int(input("input title_position"))
    language=int(input("0 means chinese"))
    JR=int(input("input position"))
    filename=filepath+"，"+str(year)+".xlsx"
    print(filename)
    write_out=str(year)+"_"+str(page)+".xlsx"
    dict_temp=pd.read_excel(filename,sheet_name=0)
    transfer=[]
    
    for i in range(1,len(dict_temp)):
        dict_list={}
        title_keyword=keyword(dict_temp.iloc[i, title_position],keywords[language])
        if title_keyword:
            if dict_temp.iloc[i, JR]:
                name=dict_temp.iloc[i, JR]
                dict_list['期刊名']=name
            else:
                dict_list['期刊名']=name
            dict_list['文章名']=dict_temp.iloc[i, title_position]
            dict_list['关键词']=title_keyword
            dict_list['年份']=str(year)
            transfer.append(dict_list)
    df = pd.DataFrame(transfer)
    df.to_csv(write_out, index=False)
    print(write_out)
main()
