# -*- coding: utf-8 -*-
from Queue import Queue
from bs4 import BeautifulSoup
import time
import threading
import requests
import re
import MySQLdb
url_queue = Queue()
page_queue = Queue()
announURL_queue = Queue()
save_queue = Queue()

re_date = re.compile(r'</a>.*?(\d{4}-\d{2}-\d{2})',re.DOTALL)
SQL_CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS shandongGP(_id INT PRIMARY KEY AUTO_INCREMENT,title VARCHAR (256) NOT NULL,publisher VARCHAR (256) NOT NULL,publishdate DATE NOT NULL,article TEXT (10240) NOT NULL,article_url VARCHAR (256) NOT NULL)'
SQL_INSERT = "INSERT INTO shandongGP(title,publisher,publishdate,article,article_url) VALUES(%s,%s,%s,%s,%s)"
class UrlThread(threading.Thread):
    def run(self):
        while(True):
            try:
                r = requests.get(url_queue.get())
                r.raise_for_status
                time.sleep(1)
                r.encoding = r.apparent_encoding
                page_queue.put(r.text)
            except:
                continue
class parserThread(threading.Thread):
    def run(self):
        while(True):
            self._parse_announ_list()
    def _parse_announ_list(self):
        soup = BeautifulSoup(page_queue.get(), "html.parser")
        
        tds = soup.findAll('td',{'class':'Font9'})
        for td in tds:
            try:
                a = td.find('a',{'class':'aa'})
                aURL = 'http://www.ccgp-shandong.gov.cn' + a.attrs['href']
                title = a.attrs['title']
                date = re_date.findall(str(td))[0]
                announURL_queue.put([aURL,title,date])
                print aURL
            except: 
                continue
       
class parseAnnounThread(threading.Thread):
    def run(self):
        while(True):
            try:
                announ_list = announURL_queue.get()
                anurl = announ_list[0]
                
                r = requests.get(anurl)
                r.raise_for_status
                r.encoding = r.apparent_encoding
                soup = BeautifulSoup(r.text, "html.parser")
                message = soup.find('td',{'class','aa'}).get_text().strip()
                td = soup.find('td',{'class':'Font9'})
                announ_type = td.get_text().split(u'\uff1a')[1]
                save_queue.put([announ_list[1],announ_list[2],message,announ_type])
            except:
                print "error1"
                
                
class saveDBThread(threading.Thread):                
    def run(self):
        while(True):
            try:
                save_list = save_queue.get()
                conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='114514', db='mydb', charset='utf8')
                #SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS articleku(_id INT PRIMARY KEY AUTO_INCREMENT,title VARCHAR(256) NOT NULL,announ_date DATE NOT NULL,message TEXT(10240) NOT NULL,announ_type VARCHAR(64) NOT NULL);"
                SQL_INSERT = "INSERT INTO articleku(title,announ_date,message,announ_type) VALUES(%s,%s,%s,%s)"
                cursor = conn.cursor()
                #cursor.execute(SQL_CREATE_TABLE)
                cursor.execute(SQL_INSERT,[save_list[0],save_list[1],save_list[2],save_list[3]])
                cursor.close()
                conn.commit()
                conn.close()
            except:
                print "error2"
        
def setDept(dept_tender):
    for i in range(dept_tender):
        url = "http://www.ccgp-shandong.gov.cn/sdgp2014/site/channelall.jsp?curpage=%s&colcode=0304"%(i+1)
        url_queue.put(url)

def main():
    s_html = UrlThread()  #获取公告列表页HTML
    s_html.start()
    setDept(20)   #设置爬取页数（招标，更改，结果）
    s_list_page = parserThread() #解析列表页（获取标题，日期，公告URL）
    s_list_page.start()
    
    s_announ = []              #解析公告页（获取公告正文，公告类型）
    for j in range(4):  #range内设置解析公告页线程个数
        s_announ.append(parseAnnounThread())  
        s_announ[j].start()
    s_save = saveDBThread()
    s_save.start()
main()



'''
            conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='114514', db='mydb', charset='utf8')
            
            cursor = conn.cursor()
            #cursor.execute(SQL_CREATE_TABLE)
            while(True):
                try:
                    cursor.execute(SQL_INSERT,[announ_list[1],itemannoun_type,announ_list[2],message,aURL])
         
                except Exception as e:
                    if len(message) > 10240:   #若公告过长则截取前一部分和后一部分，继续循环
                        message = message[0:5119] + message[-5119:]
                        continue
                    else:                      #若为其他异常则回滚然后结束循序  
                        conn.rollback()
                        break
                else:                          #若不抛异常，则正常提交
                    conn.commit()
                    break
            
            cursor.close()
            conn.close()'''
