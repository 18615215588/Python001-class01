import requests

if __name__ == "__main__":
    url = "https://www.douban.com"
    resp = requests.get(url, headers={})
    print(resp.status_code)