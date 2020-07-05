# -*- coding: utf-8 -*-
import scrapy
import redis3
from .. import items


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    #start_urls = ['https://maoyan.com/films?showType=3']  #定义爬虫开始爬取页面的起点url

    def _err_back(self, failure):
        with redis3.Redis(host='192.168.3.90', port=6379, db=0, password="heiheiredis") as rds:
            rds.lpush("err_list", "_err_back_error:{}".format(repr(failure)))

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse, errback=self._err_back, dont_filter=True)

    def parse(self, response: "Response") -> "Requests or Items":
        """
        对scrapy请求的网页回应进行处理，获取有用信息
        """
        #print("获取到响应：{}".format(response.text))
        selector = scrapy.Selector(response=response)  #创建一个Selecter对象，使用XPath获取网页元素
        mov_all_info = selector.xpath('//div[@class="movie-item-hover"]')[:10]  #获取前十个电影信息
        mov_info_list = (
            items.MaoyanMysqlItem(
                title=mov_info.xpath('.//div[@class="movie-hover-info"][1]/div[@class="movie-hover-title"][1]/span[1]/text()')[0].get(),                      #电影名称
                mov_type=mov_info.xpath('.//div[@class="movie-hover-info"][1]/div[@class="movie-hover-title"][2]/text()').getall()[1].strip(),                #电影类型
                date=mov_info.xpath('.//div[@class="movie-hover-info"][1]/div[@class="movie-hover-title movie-hover-brief"][1]/text()').getall()[1].strip()   #电影上映日期
            ) 
            for mov_info in mov_all_info
        )
        return (mov for mov in mov_info_list)
