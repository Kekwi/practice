# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS articleku(_id INT PRIMARY KEY #AUTO_INCREMENT,publisherText VARCHAR(64) NOT NULL,publishTimeText #VARCHAR(256) NOT NULL,message TEXT(10240) NOT NULL);"
#,item['PUBLISHER'],item['PUBLISH_DATE'],item['ARTICLE'],item['ARTICLE_URL']
#,%s,%s,%s,%s
#,publishdate,publisher,article,article_url
import pymysql
class GpannounPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='douyucrawler', charset='utf8')
        SQL_CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS articlekutest(_id INT PRIMARY KEY AUTO_INCREMENT,title VARCHAR (256) NOT NULL,publisher VARCHAR (256) NOT NULL,publishdate VARCHAR (256) NOT NULL,article TEXT (10240) NOT NULL,article_url VARCHAR (256) NOT NULL)'
        SQL_INSERT = "INSERT INTO articlekutest(title,publisher,publishdate,article,article_url) VALUES(%s,%s,%s,%s,%s)"
        cursor = conn.cursor()
        cursor.execute(SQL_CREATE_TABLE)
        cursor.execute(SQL_INSERT,[item['TITLE'],item['PUBLISHER'],item['PUBLISH_DATE'],item['ARTICLE'],item['ANNOUN_URL']])
        cursor.close()
        conn.commit()
        conn.close()
        return item
