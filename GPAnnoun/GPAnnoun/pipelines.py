# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class GpannounPipeline(object):
    #连接并保存到数据库
    def process_item(self, item, spider):
        DBKWARGS = spider.settings.get('DBKWARGS')
        conn = pymysql.connect(**DBKWARGS)
        SQL_CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS articlekutest(_id INT PRIMARY KEY AUTO_INCREMENT,title VARCHAR (256) NOT NULL,publisher VARCHAR (256) NOT NULL,publishdate DATE NOT NULL,article TEXT (10240) NOT NULL,article_url VARCHAR (256) NOT NULL)'
        SQL_INSERT = "INSERT INTO articlekutest(title,publisher,publishdate,article,article_url) VALUES(%s,%s,%s,%s,%s)"
        
        cursor = conn.cursor()
        cursor.execute(SQL_CREATE_TABLE)
        
        while(True):
            try:
                cursor.execute(SQL_INSERT,[item['TITLE'],item['PUBLISHER'],item['PUBLISH_DATE'],item['ARTICLE'],item['ANNOUN_URL']])
            except Exception as e:
                if len(item['ARTICLE']) > 10240:         #若公告过长则截取前一部分和后一部分，继续循环
                    item['ARTICLE'] = (item['ARTICLE'])[0:5119] + (item['ARTICLE'])[-5119:]
                    continue
                else:                                    #若为其他异常则回滚然后结束循序  
                    conn.rollback()
                    break
            else:                                        #若不抛异常，则正常提交
                conn.commit()
                break
        
        cursor.close()
        conn.close()    
        return item
