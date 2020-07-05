# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import redis3
import scrapy.exceptions
from scrapy import signals


class MaoyanMysqlSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MaoyanMysqlDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MaoYanMySQLProxyMiddleWare(MaoyanMysqlDownloaderMiddleware):
    """
    继承自预定义的下载中间件，实现其中部分方法，其他方法不做处理忽略
    """
    @classmethod
    def from_crawler(cls, crawler) -> MaoyanMysqlDownloaderMiddleware:
        return cls(crawler.settings.get("HTTP_PROXY_LIST"))  #从settings.py中获取设置的代理服务器列表

    def __init__(self, proxy_list: list):
        self.proxys = proxy_list

    def process_request(self, request, spider):
        proxy_to_use = random.choice(self.proxys)
        print("使用代理：{}".format(proxy_to_use))
        request.meta['proxy'] = proxy_to_use

    def process_response(self, request, response, spider):
        """
        如果请求响应的的状态存在问题，则产生一个异常由request对象的errback进行处理
        """
        if response.status >= 400 or hasattr(response,'exception'):
            raise scrapy.exceptions.IgnoreRequest("err_status:{}, err_msg:{}".format(response.status, response.text))
        return response

    def process_exception(self, request, exception, spider):
        """
        处理下载过程中出现的异常,把日志扔到redis中由专门的日志处理器处理
        处理由process_request及下载过程中引发的异常
        """
        with redis3.Redis(host='192.168.3.90', port=6379, db=0, password="heiheiredis") as rds:
            rds.lpush("err_list", "process_exception_error:{}".format(repr(exception)))