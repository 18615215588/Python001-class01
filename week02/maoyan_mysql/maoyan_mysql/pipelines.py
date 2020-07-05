# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas
import mysql
from mysql.connector import errorcode

def storage_mov_mysql(title: str, mov_type: str, date: str) -> None:
    try:
        cnx = mysql.connector.connect(
            user='zhaol', 
            password='dkjfosdkf',
            host='192.168.3.90',
            database='pythonclass',
            charset="utf8",
        )
        csr = cnx.cursor()      
        sql = "insert into maoyan_top (`mov_title`, `mov_type`, `mov_date`) values (%s, %s, %s)"
        result = csr.execute(sql, (title, mov_type, date))
        print("插入数据库，执行结果：{}".format(result))
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("访问首先，检查账户是否正确")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("数据库不存在")
        else:
            print("出现其他错误，错误：{}".format(err))
    except Exception as e:
        print("出现其他错误，错误：{}".format(repr(e)))
    finally:
        csr.close()
        cnx.close()

class MaoyanMysqlPipeline:
    def process_item(self, item, spider: "SpiderObj") -> "Item":
        print("猫眼管道处理函数：{}".format(item))
        #把电影信息写入到数据库中
        storage_mov_mysql(item["title"], item["mov_type"], item["date"])
        #写入字典到csv默认会将字典的key写入，而不是值（item是字典），先将数据进行一下处理
        # df = pandas.DataFrame(columns=["电影名称:"+item["title"],"电影类型:"+item["mov_type"],"上映日期:"+item["date"]])
        # df.to_csv("maoyan_scrapy.csv", mode="a", encoding="utf-8")
        return item
