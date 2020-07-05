# -*- coding: utf-8 -*-

# Scrapy settings for maoyan_mysql project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'maoyan_mysql'

SPIDER_MODULES = ['maoyan_mysql.spiders']
NEWSPIDER_MODULE = 'maoyan_mysql.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'maoyan_mysql (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#定义代理地址列表
HTTP_PROXY_LIST = [
    "http://52.179.231.206:80",
    "http://95.0.194.241:9090",
]

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DEFAULT_REQUEST_HEADERS = {
    'Cookie':'__mta=208417709.1592895912492.1592902918645.1592903952867.7; uuid_n_v=v1; uuid=DF9CCBB0B51F11EA801551553EAD9849A9C6A4B3E2894835A13DFBE0903318F2; _csrf=b440c76ad9bd8b530488f522785e6cf7af43ac1e907b9196a84bc71857d4234e; _lxsdk_cuid=172dffeb93ec8-0d64910ea0f05a-143e6257-1fa400-172dffeb93ec8; mojo-uuid=6a2c8527c33ed9dd8462351a67bb364e; mojo-session-id={"id":"5fa649bfa4a5fb40547b9af2b7ae5a30","time":1592898021553}; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22172e0281287bdf-06e09e70bab7de-2076244f-546797-172e0281288c3f%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22172e0281287bdf-06e09e70bab7de-2076244f-546797-172e0281288c3f%22%7D; _lxsdk=DF9CCBB0B51F11EA801551553EAD9849A9C6A4B3E2894835A13DFBE0903318F2; lt=sbcAoSSv2aNOkmQO1M30XtzxY4oAAAAA5woAAM42swSU-Amm1PnUAOMGoyjjYbuzAnq3nio6jK_ArkGALUH-whiVT6KsP7yiYWj32g; lt.sig=ytlNcmJAcMmZ5ZqM84NQiRBdoqM; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592906608,1592906937,1592906948,1592906968; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1592906968; __mta=208417709.1592895912492.1592903952867.1592906969162.8; mojo-trace-id=50; _lxsdk_s=172e01ee84e-47c-6be-c2b%7C%7C99',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'maoyan_mysql.middlewares.MaoyanMysqlSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'maoyan_mysql.middlewares.MaoyanMysqlDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'maoyan_mysql.middlewares.MaoYanMySQLProxyMiddleWare': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'maoyan_mysql.pipelines.MaoyanMysqlPipeline': 300,
#}
ITEM_PIPELINES = {
    'maoyan_mysql.pipelines.MaoyanMysqlPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
