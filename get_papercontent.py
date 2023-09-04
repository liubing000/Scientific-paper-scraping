import os
import urllib
import urllib.request
import time
import json
import xlwt
import requests
import random
import re
from bs4 import BeautifulSoup
import xlwt
import pandas as pd

header = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
          'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
           'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
          'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
          'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
           'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
           'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
           'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
           'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
           'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
           'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36']

headers = {
                  "User-Agent":header[random.randint(0,len(header)-1)],
}      


# 一共多少页文章
# 一共多少页数据
  
  # 选择PNAS期刊下的Social sciences分类，
  # 2023年应该是已经没有该分类了。
  # 抓取数据的方式可能需要改变
url = 'https://www.pnas.org/content/by/section/Social%20Sciences?' 
resp = requests.get(url,headers=headers)  # 给网址发送请求，获取       &Refer=2&page=1
resp.content.decode("utf-8") #打印网页内容 以二进制返回内容
html = resp.text
soup = BeautifulSoup(html,'html.parser') 
for i in soup.find_all('li',{'class':'pager-last last'}):
    pagenum_text = i.find('a')['href']
    page_num = int(pagenum_text.split('=')[-1])
    print(page_num)
# 一共多少页的数据

# pnas杂志社会科学一共347页文章
# 对每页文章进行爬取
file = 'all_data.txt'
# 每页包含的文章
for i in range(int(page_num)+1):
    url =  'https://www.pnas.org/content/by/section/Social%20Sciences?page='+str(i) 
    resp = requests.get(url,headers=headers)  # 给网址发送请求，获取       &Refer=2&page=1
    resp.content.decode("utf-8") #打印网页内容 以二进制返回内容
    html = resp.text
    soup = BeautifulSoup(html,'html.parser') 
    article = soup.find("div",{"class":"highwire-list highwire-article-citation-list"})
    article = article.find_all('span',{'class':'highwire-cite-title'})
    # article中保存的就是文章标题了
    # 当前页有多少篇文章
    # baocun 基础信息 
        # journal保存发表杂志
        # date出版时间
        # volume
        # issue 
        # pages
        # doi
        # doi链接点进去就可以看到文章内容
        # 可以爬取pdf或者摘要
    base_information = soup.find_all('div',{'class':'highwire-cite-metadata'})
    #len(base_information)
    
    # 保存当页数据 第i页
    print('保存' + str(i) +'页文章信息！')
    for j in range(len(article)):
        # 提取标题
        title = article[j].text
        print(title)

        base_infor = base_information[j].text
        print(base_infor)
        
        # 保存文本
        with open(file,'a',encoding='utf-8') as fh:
            fh.write(str(i)+'\t'+str(j)+'\t'+str(title)+'\t'+str(base_infor)+'\n')
    time.sleep(2)


# 将txt转换为csv
def txt_csv(filename,csvname):
    try:
        with open(filename,'r',encoding='utf-8') as f:
            csv=xlwt.Workbook()
             #生成excel的方法，声明excel
            sheet = csv.add_sheet('sheet1',cell_overwrite_ok=True)
            # 页数、条数、微博地址、发布时间、微博内容、点赞数、评论数、转发数
            sheet.write(0, 0, '爬取页数')
            sheet.write(0, 1, '爬取当前页数的条数')
            sheet.write(0, 2, 'title')
            sheet.write(0, 3, 'base_infor')
            x = 1
            while True:
                #按行循环，读取文本文件
                line = f.readline()
                if not line:
                    break  #如果没有内容，则退出循环
                for i in range(0, len(line.split('\t'))):
                    item=line.split('\t')[i]
                    sheet.write(x,i,item) # x单元格行，i 单元格列
                x += 1 #excel另起一行
        csv.save(csvname) #保存xls文件
    except:
        raise

filename = 'all_data.txt'
csvname = 'all_data.csv'
txt_csv(filename,csvname)


# 如此获得的是文章的title和base information
# 需要根据doi url获得关键字、摘要文本

df = pd.read_csv('all_data.csv')
for i in range(0,3417):   
    df['doi'][i] = 'https://doi.org/10.1073/pnas.' + df.iloc[i]['base_infor'].split('pnas.')[1].split('\n')[0].replace(' ','')
# 删除重复行
df = df.drop_duplicates(['doi'],keep='first')


# 使用doi链接获取关键字内容
# 对所有的doi进行
for j in range(df.shape[0]):
        # 针对doi链接 
        # 爬取其他信息
        doi_url = df['doi'][j]
        headers = {
                  "User-Agent":header[random.randint(0,len(header)-1)]}
        # 设置代理IP
        #proxy_addr="180.97.87.63:80"
        #proxy = {'http':proxy_addr}
       # resp = requests.get(doi_url,headers=headers,proxies=proxy)  
        resp = requests.get(doi_url,headers=headers) 
        resp.content.decode("utf-8") #打印网页内容 以二进制返回内容
        html = resp.text
        soup = BeautifulSoup(html,'html.parser') 
        time.sleep(2)
        
        # 保存摘要
        abstract = soup.find('div',{'class':'section abstract'})
        if abstract == None:
            abstract = ''
        else:
            abstract = abstract.text
            abstract = soup.find('div',{'class':'section abstract'})
            abstract = abstract.text.split('Abstract')[1]
        # print(abstract)

        # 保存题目
        title = soup.find('h1',{'class':'highwire-cite-title'})
        if title == None:
            title = ''
        else:
            title = title.text
        print(title)

        # 保存关键字
        k = soup.find_all('li',{'class':'kwd'})
        keywords = []
        for i in k:
            keywords.append(i.text)
        # print(soup.find_all('li',{'class':'last'})[-5].find('a')['href'])
        
        # 保存pdf下载链接
        t = soup.find_all('li',{'class':'last'})
        #print(t)
        if t != [] :
            pdf_link = 'pnas.org'+soup.find_all('li',{'class':'last'})[-5].find('a')['href']
        else:
            pdf_link = ''
        
        print('当前爬取第'+str(j)+'条文章内容!')
        # 保存文本
        with open(file,'a',encoding='utf-8') as fh:
            fh.write(str(j)+'\t'+str(df['title'][j])+'\t'+str(title.replace('\n',' '))+'\t'+str(abstract.replace('\n',' '))+'\t'+str(keywords)+'\t'+str(doi_url)+'\t'+str(pdf_link)+'\n')

# 当前内容从txt转换为csv
def txt_csv(filename,csvname):
    try:
        with open(filename,'r',encoding='utf-8') as f:
            csv=xlwt.Workbook()
             #生成excel的方法，声明excel
            sheet = csv.add_sheet('sheet1',cell_overwrite_ok=True)
            # 页数、条数、微博地址、发布时间、微博内容、点赞数、评论数、转发数
            sheet.write(0, 0, '爬取条数')
            sheet.write(0, 1, 'title')
            sheet.write(0, 2, 'title_1')
            sheet.write(0, 3, 'abstract')
            sheet.write(0, 4, 'keywords')
            sheet.write(0, 5, 'doi_link')
            sheet.write(0, 6, 'pdf_link')
            x = 1
            while True:
                #按行循环，读取文本文件
                line = f.readline()
                if not line:
                    break  #如果没有内容，则退出循环
                for i in range(0, len(line.split('\t'))):
                    item=line.split('\t')[i]
                    sheet.write(x,i,item) # x单元格行，i 单元格列
                x += 1 #excel另起一行
        csv.save(csvname) #保存xls文件
    except:
        raise

filename = 'keywords.txt'
csvname = 'keywords.csv'
txt_csv(filename,csvname)