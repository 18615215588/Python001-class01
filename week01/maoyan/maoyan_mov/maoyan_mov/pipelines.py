# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas 

class MaoyanMovPipeline:
    def process_item(self, item, spider):
        print("猫眼管道处理函数：{}".format(item))
        #写入字典到csv默认会将字典的key写入，而不是值（item是字典），先将数据进行一下处理
        df = pandas.DataFrame(columns=["电影名称:"+item["title"],"电影类型:"+item["mov_type"],"上映日期:"+item["date"]])
        df.to_csv("maoyan_scrapy.csv", mode="a", encoding="utf-8")
        return item
