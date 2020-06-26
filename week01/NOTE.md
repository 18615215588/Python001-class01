学习笔记
1.使用requests库进行HTTP网络请求，获取回应对象进行处理  
2.使用beautifulsoup4库对requests库获取的response进行分析处理，生成HTML的文档数据结构  
3.bs4库可以使用find或find_all来根据标签名称和绑定属性获取HTML Tag对象，通过这种方式可以对抓取的网页进行数据提取  
4.使用lxml库，可以使用xpath语法来对HTML文档结构进行解析，xpath处理起来更方便  
5.使用scrapy爬虫框架对以上requests+bs4的爬取方式进行替换，scrapy框架是一套完整的爬虫框架，集成了完善的网络爬虫功能集  
    scrapy框架由：引擎，调度器，下载器，爬虫，项目管道，下载器中间件，爬虫中间件组成  
    其中需要进行定义的主要是：spdiers，项目管道，Item定义  
    spiders：进行HTTP请求获取响应，对响应进行解析，返回后续请求或Item发送到管道进行持久化  
    pipeline：对引擎发来的Item进行分析处理，验证数据有效性，并进行相应持久化  
    Item：对爬虫爬取的HTML文档信息进行结构化定义  
#scrapy startproject xxx                //创建一个scrapy项目，会生成一些配置和代码  
#cd xxx & scrapy genspider xxx xxx.com  //进入项目目录，并生成一个名为xxx的爬虫  
#scrapy crawl xxx                       //运行指定爬虫对网页进行爬取  
settings.py文件中包含了很多爬虫配置参数：  
1.用户代理：设置一个模仿真正浏览器的用户代理  
2.其他头信息：设置一些有用的头信息用于防反爬  
3.设置pipeline：指定要处理Item的管道及优先级  
....  
*xpath:
"//xxx":从上往下依次查找指定标签  
"/xxx":绝对路径，表示根节点下的标签  
"//xxx[@class="xxx"]":查找绑定了class属性的标签元素  
使用xpath可以很方便的根据文档标签的上下级关系对文档进行检索  
Selector：scrapy中可以使用Selector利用xpath对文档进行检索，查找想要的信息  
