# -*- coding: utf-8 -*-
import scrapy
from .. import items

def print_iterator(i : "Iterator") -> None:
    for v in i:
        print("迭代元素：{}".format(v))


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        selector = scrapy.Selector(response=response)
        mov_all_info = selector.xpath('//div[@class="movie-item-hover"]')
        #文本内容有可能因为格式问题而导致出现多元素的情况，可以通过getall获取所有文本然后处理
        mov_info_list = (items.MaoyanMovItem(title=mov_info.xpath('.//div[@class="movie-hover-info"][1]/div[@class="movie-hover-title"][1]/span[1]/text()')[0].get(), mov_type=mov_info.xpath('.//div[@class="movie-hover-info"][1]/div[@class="movie-hover-title"][2]/text()').getall()[1].strip(), date=mov_info.xpath('.//div[@class="movie-hover-info"][1]/div[@class="movie-hover-title movie-hover-brief"][1]/text()').getall()[1].strip()) for mov_info in mov_all_info)
        return list(mov_info_list)[:10]
