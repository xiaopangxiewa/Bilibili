# -*- coding: utf-8 -*-
import scrapy
from bilibili.items import BilibiliItem
from scrapy.http import Request
import re


class BiliSpider(scrapy.Spider):
    name = "bili"
    allowed_domains = ["bilibili.com"]
    #start_urls = ['http://bilibili.com/']
    def start_requests(self):
        s_url='https://www.bilibili.com/video/av14095964/?spm_id_from=333.334.bili_music.11'
        #这里可以不要的，不想删
        yield Request(s_url,callback=self.parse)

    def parse(self, response):
        a=response.body.decode('utf-8','ignore')
        print(len(a))
        v_id='jQuery17205371969976539306_1511357504211'
        #视频id需抓包分析得到，fiddler4简单好用易入门
        for i in range(1,3):  #这里只爬取了评论的前两页，如果要爬取多页，更改数字即可
            c_url='https://api.bilibili.com/x/v2/reply?callback=%s&jsonp=jsonp&pn=%d&type=1&oid=14095964'%(v_id,i)
            
            yield Request(c_url,callback=self.next,dont_filter=True)
    def next(self,response):
        print('请求成功')
        a=response.body.decode('utf-8','ignore')
        item=BilibiliItem()
        print(len(a))
        pat1='"uname":"(.*?)"'
        pat2='"sex":"(.*?)"'
        pat3='"sign":"(.*?)"'
        pat4='"message":"(.*?)"'
        item['uname']=re.compile(pat1).findall(a)
        item['usex']=re.compile(pat2).findall(a)
        item['usign']=re.compile(pat3).findall(a)
        item['ucomment']=re.compile(pat4).findall(a)
        return item
        
        
        
        
