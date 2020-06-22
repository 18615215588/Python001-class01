import requests
import bs4

if __name__ == "__main__":
    url = "https://movie.douban.com/top250"
    #防止反爬程序返回418
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    headers = {"user-agent":user_agent}

    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    bs_info = bs4.BeautifulSoup(resp.text, "html.parser")
    all_div_element = bs_info.find_all("div", {"class":"hd"})
    print(type(all_div_element))  #all_div_element是bs4.element.ResultSet类型
    for e in all_div_element:
        print(type(e))
    content = ((a.get("href"),a.find("span").text) for e in all_div_element for a in e.find_all('a'))
    for href in content:
        print(href)