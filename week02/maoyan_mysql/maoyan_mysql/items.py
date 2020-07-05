# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanMysqlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    mov_type = scrapy.Field()
    date = scrapy.Field()

    def __str__(self):
        return "电影名称：{}, 电影类型：{}, 上映日期：{}".format(self['title'], self['mov_type'], self['date'])

