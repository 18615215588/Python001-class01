import requests
import bs4
import random
import pandas

maoyan_url = "https://maoyan.com/films?showType=3"  #猫眼热门电影的信息列表页URL

#定义header信息，随机选择一个
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

#定义headers,定义Referer来源放反爬
headers = {
    "User-Agent":random.choice(user_agent),
    'Cookie':'__mta=222122535.1593142612666.1593142847141.1593142870733.9; uuid_n_v=v1; uuid=46318240B75E11EA9C0AF732B1940F47A9A76B57EC6A4BE3A7DD92F2C403AB0A; _csrf=c31ce07eb8faab105663ad62a516058cd6b047979b0770110547127735f7c5d1; mojo-uuid=c6b8eb14bb2f3bc501074e94b8074f9c; _lxsdk_cuid=172eeb31223c8-07bc15662ca93c-4353760-1bcab9-172eeb3122395; _lxsdk=46318240B75E11EA9C0AF732B1940F47A9A76B57EC6A4BE3A7DD92F2C403AB0A; mojo-session-id={"id":"d92f353ffc75eaa9580519f8974943c0","time":1593142612536}; lt=NGasidSZ6zE6ovA8CG95KS-_rIQAAAAA5woAAA55z4CS3rvkpsKkv2GYbmTFuB37EgqV3pC5Cmh2WN6mJ8IOPFgebttlkYAd3MOG7w; lt.sig=XB09fEDTRPnAVsOyo4IJJAxXq5s; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593142630,1593147432,1593147698,1593147812; mojo-trace-id=23; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593149271; __mta=222122535.1593142612666.1593142870733.1593149271077.10; _lxsdk_s=172eeb31225-e42-e97-639%7C%7C46',
    "Referer":"https://www.maoyan.com/",
}

#根据url获取Response
def get_url(url : str) -> "Response":
    return requests.get(url, headers=headers)

#显示迭代对象
def print_iterator(i : "Iterator") -> None:
    for v in i:
        print(v)

#电影信息类
class MovieInfo():
    def __init__(self, title: str, mov_type: str, date: str) -> None:
        self._title = title
        self._mov_type = mov_type
        self._date = date
    @property
    def title(self) -> str:
        return self._title
    @title.setter
    def title(self, value: str) -> None:
        self._title = value
    @property
    def mov_type(self) -> str:
        return self._mov_type
    @mov_type.setter
    def mov_type(self, value:str) -> None:
        self._mov_type = value
    @property
    def date(self) -> str:
        return self._date
    @date.setter
    def date(self, value:str) -> None:
        self._date = value
    def __repr__(self):
        return "<MovieInfo Object: title:{}, type:{}, date:{}>".format(self.title, self.mov_type, self.date)
    def __str__(self):
        return "[电影名称：{}, 电影类型：{}, 上映日期：{}]".format(self.title, self.mov_type, self.date)


#主业务流程
if __name__ == "__main__":
    try:
        mov_all_resp = get_url(maoyan_url)
        mov_all_resp.encoding = "utf-8"
        if mov_all_resp.status_code != 200:
            print("Http Request Error, Status Code:{}".format(mov_all_resp.status_code))
            raise Exception("Http Request Error, Status Code:{}".format(mov_all_resp.status_code))      
        mov_all_info = bs4.BeautifulSoup(mov_all_resp.text, features="html.parser").find_all("div", {"class":"movie-item film-channel"}) #解析热门电影信息页面
        mov_info_list = (MovieInfo(mov_info.find("span", {"class":"name"}).text, mov_info.find_all("div", {"class":"movie-hover-title"})[1].text.split(":")[-1].strip(), mov_info.find_all("div", {"class":"movie-hover-title movie-hover-brief"})[0].text.split(":")[-1].strip()) for mov_info in mov_all_info)
        #将获取到的信息写入csv文件
        df = pandas.DataFrame(list(mov_info_list)[:10])
        df.to_csv("maoyan_requests.csv", encoding="utf-8")
    except Exception as e:
        print("Exception Raised，Exception：{}".format(e))