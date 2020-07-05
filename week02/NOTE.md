学习笔记

1.常见异常类型：
LookupError下的IndexError和KeyError
IOError，NameError，TypeError，AttributeError，ZeroDivisionError

2.异常处理：
try:
except Exception as e:
finally:
自定义异常继承自Exception类

3.优化异常显示格式：
使用第三方库：pretty_errors

4.反反爬虫：
User-Agent设置，Referer：防止跨站，Cookie

5.模拟浏览器行为：
使用第三方库：selenium
通过不同浏览器插件，启动本机浏览器模拟各种输入点击操作。
可以通过名称，id，xpath等方式检索html元素

6.访问MySQL
使用第三方库：PyMySQL库
首先，根据用户名密码等参数建立到数据库的连接，连接可以复用
然后，创建一个游标对象，游标对象支持上下文管理器协议，可以使用with语句
使用execute执行参数化的SQL语句将数据插入到数据库中

7.通过使用中间件来对Scrapy的请求对象进行定制，可以实现多个代理自由切换
为了能够在出现请求异常时处理异常，需要对下载中间件进行定制，实现process_exception方法
对于处理response时出现的错误，可以实现定制request对象的errback回调函数实现处理

8.分布式爬虫
将scrapy的信息存储在redis中，多个scrapy实例共享这些信息，实现分布式爬虫，使用scrapy-redis第三方库实现
