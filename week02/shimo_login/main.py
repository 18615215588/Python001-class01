import selenium.webdriver as wd
import time

try:
    bsr = wd.Chrome()
    bsr.get("https://shimo.im/login?from=home")
    time.sleep(3)
    bsr.find_element_by_name("mobileOrEmail").send_keys("*********")
    bsr.find_element_by_name("password").send_keys("*********")
    time.sleep(3)
    bsr.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button").click()
    cookies = bsr.get_cookies()
    print("登录之后的Cookie为：{}".format(cookies))
    time.sleep(5)
except Exception as e:
    print("卧槽！出错啦，错误：{err}".format(err=repr(e)))
finally:
    bsr.close()


