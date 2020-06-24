# -*- coding: utf-8 -*-
import scrapy
import bs4
from .. import items

def print_iterable(i : "Iterable"):
    for v in i:
        print(v)


class MovieSpider(scrapy.Spider):
    name = 'movie'                                          #spider的唯一标识，不能重复，启动爬虫时需要用到
    allowed_domains = ['douban.com']                        #限定域名，只能爬取该域名下的网页
    start_urls = ['https://movie.douban.com/top250']        #第一次请求所使用的URL，列表，可以包含多个URL

    #spider启动时只执行一次，必须返回一个可迭代对象，因为只执行一次，可以将其写为一个包含yield语句的生成器函数
    def start_requests(self):
        yield from map(lambda url: scrapy.Request(url, callback=self.parse), (f"https://movie.douban.com/top250?start={page * 25}&filter=" for page in range(0, 10)))

    #默认的请求响应回调函数，必须返回一个包含Request对象的可迭代对象或包含Item对象的字典
    def parse(self, response):
        #print(response)
        bs_info = bs4.BeautifulSoup(response.text, features="html.parser")
        movie_urls = (div_hd.a['href'] for div_hd in bs_info.find_all("div", {"class": "hd"}))         #解析所有电影信息标签，返回一个生成器，生成器只能一次使用
        movie_names = (div_hd.span.string for div_hd in bs_info.find_all("div", {"class": "hd"}))      #解析所有电影名称，返回一个生成器，生成器只能一次使用
        #print_iterable(movie_urls)  #打印后，生成器已经被消费，无法再次使用
        #print_iterable(movie_names) #打印后，生成器已经被消费，无法再次使用
        yield from (scrapy.Request(url, callback=self.parse_mov_detail) for url in movie_urls)         #从生成器中得到url，创建Request，并生成新的生成器
        #yield from ({"mov_name": name} for name in movie_names)

    #处理解析每个电影详细信息函数
    def parse_mov_detail(self, response):
        bs_info = bs4.BeautifulSoup(response.text, features="html.parser")
        mov_name = bs_info.find_all("h1")[0].span.string  #获取电影名称
        mov_year = bs_info.find_all("h1")[0].find_all("span", {"class":"year"})[0].string
        div_mov_info = bs_info.find_all("div", {"id":"info"})[0]  #获取电影详细信息div
        mov_director = div_mov_info.find_all("a", {"rel":"v:directedBy"})[0].string
        item = items.DoubanItem()
        item['mov_name'] = mov_name
        item['mov_year'] = mov_year
        item['mov_director'] = mov_director
        #print(item)
        yield item

