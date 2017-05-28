import requests
import re
import pymysql

def getHtmlText(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print("error")
		return "";
		

def parsePage(ilt, html):
	try:
		tlt = re.findall(r'<div class=\"s_tit\"><a href=\".*?\" target=\"_blank\">(.*?)</a>', html)
		uat = re.findall(r'<div class=\"s_tit\"><a href=\"(.*?)\"', html)
		dlt = re.findall(r'<span class="list_title_r"> (\[\d{4}-\d{2}-\d{2}\])</span>', html)
		for i in range(len(tlt)):
			datemsg = dlt[i]
			title = tlt[i]
			url_atr = uat[i]
			ilt.append([datemsg, title, url_atr])
	except:
		return ""
		
def printAtcList(ilt):
	tplt = "{:4}\t{:8}\t{:16}"
	print(tplt.format("序号", "日期", "名称"))
	count = 0
	for g in ilt:
		count += 1
		print(tplt.format(count, g[0], g[1]))
def saveIntoDB(ilt):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='douyucrawler', charset='utf8')
	tplt = "{:4}\t{:8}\t{:16}"
	count = 0
	SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS pysqltest(_id INT PRIMARY KEY AUTO_INCREMENT,datemsg VARCHAR(64) NOT NULL,title VARCHAR(256) NOT NULL,url_atr VARCHAR(256) NOT NULL);"
	SQL_INSERT = "INSERT INTO pysqltest(datemsg,title,url_atr) VALUES(%s,%s,%s)"
	cursor = conn.cursor()
	cursor.execute(SQL_CREATE_TABLE)
	for g in ilt:
		count += 1
		print(tplt.format(count, g[0], g[2]))
		cursor.execute(SQL_INSERT,[g[0],g[1],g[2]])
	cursor.close()
	conn.commit()
	conn.close()

def main():
	dept = 2
	start_url = "http://i2.guet.edu.cn/jwb/list.asp?id=17&PageNo="
	infoList = []
	for i in range(dept):
		try:
			url = start_url + str(i+1)
			html = getHtmlText(url)
			parsePage(infoList, html)
		except:
			print("error")
			continue
			
	#printAtcList(infoList)
	saveIntoDB(infoList)
	
main()