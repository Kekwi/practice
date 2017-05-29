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
		return""
		

def getAnnouncementURL(html, ulist):

		soup = BeautifulSoup(html, "html.parser")
		a = soup.findAll('a', {'class':'aa'})
	
		for i in a:
			try:
				aURL = 'http://www.ccgp-shandong.gov.cn' + i.attrs['href']
				title = i.attrs['title']
				ulist.append(aURL)
			except:
				continue
		
		#<div style="text-align:center; margin:15px 0;">发布时间：2017-05-22 新闻来自：教务部 点击数：91</div>
def parseAnnouncementPage(ulist,pageInfoList):
	count = 0
	tplt = "{}\t{}\t{}"
	
	for i in ulist:
		article_html = getHtmlText(i)
		soup = BeautifulSoup(article_html, "html.parser")
		message = soup.find('td',{'class','aa'}).get_text()
		replace_reg = re.compile(r'\xa0|\u3000')
		announceInfo = soup.findAll('td',{'class':'Font9'})
		count1 = 0;
		publisherText = ""
		publishTimeText = ""
		#print(announceInfo[0])
		if len(announceInfo) == 0:
			print(i)
			publisherText = "error"
			publishTimeText = i
			message = "error"
		else:
			for j in announceInfo:
				if count1 == 0:
					publisherText = j.get_text()
					count1 += 1
				else:
					publishTimeText = j.get_text()
		#publisherText = announceInfo[0]
		#publishTimeText = announceInfo[1]
		#publisherText = "asdfad"
		#publishTimeText = "5412.454" 
		message = replace_reg.sub(' ',message)
		count += 1
		print(tplt.format(count, publisherText, publishTimeText))
		pageInfoList.append([publisherText, publishTimeText,message])

	
def saveInfoIntoDB(pageInfoList):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='douyucrawler', charset='utf8')
	count = 0
	SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS articleku(_id INT PRIMARY KEY AUTO_INCREMENT,publisherText VARCHAR(64) NOT NULL,publishTimeText VARCHAR(256) NOT NULL,message TEXT(10240) NOT NULL);"
	SQL_INSERT = "INSERT INTO articleku(publisherText,publishTimeText,message) VALUES(%s,%s,%s)"
	cursor = conn.cursor()
	cursor.execute(SQL_CREATE_TABLE)
	for k in pageInfoList:
		count += 1
		cursor.execute(SQL_INSERT,[k[0],k[1],k[2]])
	cursor.close()
	conn.commit()
	conn.close()
	
def main():

	dept = 20
	start_url = "http://www.ccgp-shandong.gov.cn/sdgp2014/site/channelall.jsp?colcode=0304&curpage="
	urlList = []
	pageInfoList = []
	for i in range(dept):
		try:
			page_url = start_url + str(i+1)
			html = getHtmlText(page_url)
			getAnnouncementURL(html, urlList)
		except:
			print("error1")
			continue
	
	
	parseAnnouncementPage(urlList, pageInfoList)
	
	saveInfoIntoDB(pageInfoList)
	
main()