import random
import itertools
import time
import requests
import bs4
import lxml
import pandas as pd

def print_iterable(i : "Iterable"):
    for v in i:
        print(v)

def get_url(url : str, headers : str) -> str:
    resp = requests.get(url, headers={"user-agent":headers}) #获取url信息
    print("请求url：{}，请求头：{}".format(url, headers))
    if resp.status_code != 200:
        raise Exception("请求http出现错误，响应码为：{}，相应信息：{}".format(resp.status_code, resp.text))
    return resp.text

#获取电影详细信息url的list
def get_movie_list(movie_list_html : str) -> list:
    bs_info = bs4.BeautifulSoup(movie_list_html, features="html.parser")  #根据传入的电影信息页的html代码解析一个bs对象
    movie_url_list = (a['href'] for div in bs_info.find_all("div", {"class": "hd"}) for a in div.find_all("a"))  #查找该页所有电影信息的div
    return movie_url_list

#根据传入的电影详细信息html，解析出电影详细信息，返回一个字典
def get_movie_detail(movie_detail : str) -> dict:
    bs_info = bs4.BeautifulSoup(movie_detail, features="html.parser")
    movie_span = bs_info.find_all('h1')[0].find_all("span")
    movie_name = movie_span[0].text
    movie_year = movie_span[1].text
    movie_info = bs_info.find_all('div', {"id":"info"})[0]
    return {"name": movie_name, "year": movie_year, "info": movie_info}


if __name__ == "__main__":
    urls = (f"https://movie.douban.com/top250?start={page * 25}&filter=" for page in range(0, 10))  #函数调用时，生成器表达式可以不加外括号
    #防止反爬程序返回418
    user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
    ]
    headers = {"user-agent":random.choice(user_agent)}  #在user_agent中随机选择一个用户代理

    #获取所有电影信息页的html代码，返回一个map对象
    movie_list = map(lambda url: get_url(url, random.choice(user_agent)), (url for url in urls)) #生成器表达式返回每个url，并用filter进行过滤
    #print_iterable(movie_list)
    #获取
    movie_info_list = map(get_movie_list, (v for v in movie_list)) #根据每一页html代码，解析电影url返回一个map对象，包含每页的电影url，每页25个url
    #print_iterable(movie_info_list)
    movie_detail_htmls = map(lambda url: get_url(url, random.choice(user_agent)), (url for page in movie_info_list for url in page))
    #print_iterable(movie_detail_htmls)
    movie_details = map(get_movie_detail, (movie for movie in movie_detail_htmls)) #根据每个详细电影信息，获取一个map，元素是每个电影的信息字典
    print_iterable(movie_details)



