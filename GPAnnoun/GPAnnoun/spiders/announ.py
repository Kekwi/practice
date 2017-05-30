# -*- coding: utf-8 -*-
import scrapy
from GPAnnoun.items import GpannounItem
import re
class AnnounSpider(scrapy.Spider):
    name = 'announ'
    count = 0
    start_urls = ['http://www.ccgp-shandong.gov.cn/sdgp2014/site/listall.jsp?colcode=0304&curpage=1']
    def start_requests(self):
        dept = 20
        reqs = []
        for i in range(dept):
            req = scrapy.Request("http://www.ccgp-shandong.gov.cn/sdgp2014/site/listall.jsp?colcode=0304&curpage=%s"%(i+1))
            reqs.append(req)
        return reqs
    def parse(self, response):
        
        AnnounSpider.count += 1
        tds = response.xpath("//tr/td[@class='Font9']")
        pcount = 0
        for td in tds:
            try:
                item = GpannounItem()
            #   item["TITLE"] = tr_tag.find('a', {'class':'aa'}).attrib['title']
                item["TITLE"] = td.xpath("a[@class='five']/@title")[0].extract()
                temp_href = td.xpath("a[@class='five']/@href")[0].extract()               
                item["ANNOUN_URL"] = 'http://www.ccgp-shandong.gov.cn' + temp_href
                t_date = td.extract()
                #self.log('-------------t_date-----item page : %s' % t_date)
                date = re.findall(r'\d{4}-\d{2}-\d{2}', t_date)
            
                item["PUBLISH_DATE"] = date
                yield scrapy.Request(url = item["ANNOUN_URL"], meta = {'item':item},callback = self.parse_detail,dont_filter = True)
            except:
                continue
				
    def parse_detail(self, response):
        item = response.meta['item']
        item["ARTICLE"] = response.xpath("string(//td[@class='aa'])")[0].extract().strip()
        item["PUBLISHER"] = response.xpath("//td[@class='Font9']/text()")[0].extract().split('：')[1]
        yield item		