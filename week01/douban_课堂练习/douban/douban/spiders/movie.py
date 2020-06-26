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
        # bs_info = bs4.BeautifulSoup(response.text, features="html.parser")
        # movie_urls = (div_hd.a['href'] for div_hd in bs_info.find_all("div", {"class": "hd"}))         #解析所有电影信息标签，返回一个生成器，生成器只能一次使用
        # movie_names = (div_hd.span.string for div_hd in bs_info.find_all("div", {"class": "hd"}))      #解析所有电影名称，返回一个生成器，生成器只能一次使用
        selector = scrapy.Selector(response=response)      #用response对象创建一个selector对象，用来解析response的html结构
        all_div_hd = selector.xpath('//div[@class="hd"]')  #从上而下获取所有带有class="hd"属性的div元素
        movie_dict = {mov_node.xpath('./a/span[1]/text()').get() : mov_node.xpath('./a[1]/@href').get() for mov_node in all_div_hd}
        #movie_names = movie_dict.keys()
        #movie_names = (mov_name_node.get() for mov_name_node in all_div_hd.xpath('./a/span[1]/text()'))  #获取电影名称
        #movie_urls = movie_dict.values()         #获取所有电影的link
        #print(all_div_hd)
        #print_iterable(movie_names)  #打印后，生成器已经被消费，无法再次使用
        #print_iterable(movie_dict.values())
        #print_iterable(movie_names) #打印后，生成器已经被消费，无法再次使用
        yield from (scrapy.Request(url, callback=self.parse_mov_detail, meta={"movie_base_info":{"name": name, "url": url}}) for name, url in movie_dict.items())         #从生成器中得到url，创建Request，并生成新的生成器
        #yield from ({"mov_name": name} for name in movie_names)

    #处理解析每个电影详细信息函数
    def parse_mov_detail(self, response):
        movie_base_info = response.meta["movie_base_info"]                                    #把上级Request传入的meta字典获取出来，里面带有每个电影基本信息，名称对应url
        mov_detail_selector = scrapy.Selector(response=response)                              #根据回应构建selector
        mov_year = mov_detail_selector.xpath('//h1[1]/span[@class="year"]/text()')[0].get()   #获取电影上映年份
        mov_info = mov_detail_selector.xpath('//div[@id="info"]')[0].get().strip()            #获取电影基本信息，删除前后空格
        mov_director = mov_detail_selector.xpath('//a[@rel="v:directedBy"]/text()')[0].get()
        item = items.DoubanItem()
        item['mov_name'] = movie_base_info["name"]
        item['mov_year'] = mov_year
        item['mov_info'] = mov_info
        item['mov_director'] = mov_director
        #print(item)
        yield item

