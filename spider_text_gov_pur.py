
import pandas as pd
import re
import os

def reg_exp(text):
    
    if not isinstance(text, str):
        text = str(text)
    answer = [None] * 4  # 初始化一个有4个元素的列表
    info = [None] * 4  
    info[0] = re.compile(r'(?:项 目 编 号|项目编号|招标文件编号|采购计划编号|项目号)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    info[1] = re.compile(r'(?:项目名称)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    info[2] = re.compile(r'(?:供应商名称)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    info[3] = re.compile(r'(?:成交金额|金额（人民币）|金额)\s*[:：]\s*(.*?)(?=\s|$)', re.DOTALL)
    
    for i in range(0,4):
        matches = None
        #显然，你想要获取所有匹配项的第一个
        matches = info[i].findall(text)
        if i==0:
            if matches:
                if len(matches)>1:
                    answer[i] = re.sub(r'^.*：', '', matches[1])  # 将第一个匹配项（是一个字符串）中“：”之前的内容删除
                else:
                    answer[i] = re.sub(r'^.*：', '', matches[0])
        else:
            if matches:
                answer[i] = re.sub(r'^.*：', '', matches[0])  # 将第一个匹配项（是一个字符串）中“：”之前的内容删除
            
    return answer
        
def path_get():
    folder_path= r'D:\myduty\workshop\cj'
    file_list = os.listdir(folder_path)
    file_path=[]
    for file in file_list:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            file_path.append(os .path.join(folder_path,file))
    return file_path
    

def read_file(filename):
    df = pd.read_excel(filename, usecols=[1, 7])
    return df


def main():
    file_path=path_get()
    for file in file_path:
        filename= os.path.basename(file)
        print(filename)
        filename1 = filename.split('.')[0] + "_copy." + filename.split('.')[1]
        print(filename1)
        dict_temp=read_file(file)
        transfer=[]
        rate = 0
        for i in range(1,len(dict_temp)):
            dict_list={}
            answer=reg_exp(dict_temp.iloc[i, 1])
            dict_list['序列号']=dict_temp.iloc[i, 0]
            dict_list['项目编号']=answer[0]
            if dict_list['项目编号']:
                rate=rate +1
            dict_list['项目名称']=answer[1]
            dict_list['供应商名称']=answer[2]
            dict_list['成交金额']=answer[3]
            transfer.append(dict_list)

        df = pd.DataFrame(transfer)
        df.to_excel(filename1, index=False)
        print("success")
        print(rate/len(dict_temp))
main()
