import requests
import re
import pymysql
import time
from bs4 import BeautifulSoup
def getHtmlText(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print("error2")
		return "";
		

def parsePage(ilt, html, ulist):
	try:
		tlt = re.findall(r'<div class=\"s_tit\"><a href=\".*?\" target=\"_blank\">(.*?)</a>', html)
		uat = re.findall(r'<div class=\"s_tit\"><a href=\"(.*?)\"', html)
		dlt = re.findall(r'<span class="list_title_r"> (\[\d{4}-\d{2}-\d{2}\])</span>', html)
		for i in range(len(tlt)):
			datemsg = dlt[i]
			title = tlt[i]
			url_atr = uat[i]
			ilt.append([datemsg, title, url_atr])
			ulist.append(url_atr)
			
	except:
		return ""
		
		#<div style="text-align:center; margin:15px 0;">发布时间：2017-05-22 新闻来自：教务部 点击数：91</div>
def parseArticlePage(ulist,pageInfoList):
	try:
		count = 0
		tplt = "{}\t{}\t{}\t{}"
		for i in ulist:
			article_html = getHtmlText(i)
			soup = BeautifulSoup(article_html, "html.parser")
			
			page = soup.find('div', {'id':'content_middle'})
			title = page.find('h1').get_text()
			info = page.find('div', {'style':'text-align:center; margin:15px 0;'}).get_text()
			release_data = re.findall(r'发布时间：(\d{4}-\d{2}-\d{2})', info)
			article_source = re.findall(r'新闻来自：(.*?) ', info)
			clicks = re.findall(r'点击数：(\d+)', info)
			articles = soup.findAll('p')
			article = ""
			for g in articles:
				article = article + g.get_text()
			replace_reg = re.compile(r'\xa0|\u3000')
			article = replace_reg.sub(' ',article)
			count += 1
			print(tplt.format(count, release_data, article_source, clicks))
			pageInfoList.append([release_data, title, article_source, clicks, article])
			
	except:
		return ""
	
def printAtcList(ilt):
	tplt = "{:4}\t{:8}\t{:16}"
	print(tplt.format("序号", "日期", "名称"))
	count = 0
	for g in ilt:
		count += 1
		print(tplt.format(count, g[0], g[1]))
		
def saveInfoIntoDB(pageInfoList):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='douyucrawler', charset='utf8')
	count = 0
	SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS articleku(_id INT PRIMARY KEY AUTO_INCREMENT,redata VARCHAR(64) NOT NULL,title VARCHAR(256) NOT NULL,artsrc VARCHAR(256) NOT NULL,click VARCHAR(256) NOT NULL,article VARCHAR(1024) NOT NULL);"
	SQL_INSERT = "INSERT INTO articleku(redata,title,artsrc,click,article) VALUES(%s,%s,%s,%s,%s)"
	cursor = conn.cursor()
	cursor.execute(SQL_CREATE_TABLE)
	for k in pageInfoList:
		count += 1
		cursor.execute(SQL_INSERT,[k[0],k[1],k[2],k[3],k[4]])
	cursor.close()
	conn.commit()
	conn.close()
	
def saveIntoDB(ilt):
	print(ilt)
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='douyucrawler', charset='utf8')
	tplt = "{:4}\t{:8}\t{:16}"
	count = 0
	SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS pysqltest(_id INT PRIMARY KEY AUTO_INCREMENT,datemsg VARCHAR(64) NOT NULL,title VARCHAR(256) NOT NULL,url_atr VARCHAR(256) NOT NULL);"
	SQL_INSERT = "INSERT INTO pysqltest(datemsg,title,url_atr) VALUES(%s,%s,%s)"
	cursor = conn.cursor()
	cursor.execute(SQL_CREATE_TABLE)
	for g in ilt:
		count += 1
		cursor.execute(SQL_INSERT,[g[0],g[1],g[2]])
	cursor.close()
	conn.commit()
	conn.close()

def main():
	dept = 24
	start_url = "http://i2.guet.edu.cn/jwb/list.asp?id=17&PageNo="
	infoAndUrl = []
	urlList = []
	pageInfoList = []
	for i in range(dept):
		try:
			url = start_url + str(i+1)
			html = getHtmlText(url)
			parsePage(infoAndUrl, html, urlList)
		except:
			print("error1")
			continue
	
	#printAtcList(infoAndUrl)
	parseArticlePage(urlList, pageInfoList)
	#saveIntoDB(infoList)
	saveInfoIntoDB(pageInfoList)
	
main()