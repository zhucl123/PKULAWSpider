from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
import random

random.seed(datetime.timestamp())
sleep = lambda : time.sleep(1 + random.uniform(0, 2))
log = lambda info : print(f"{datetime.now()}: {info}\n")

# 用于从北大法宝下载裁判文书原文
# 北大法宝提供批量下载，该爬虫是解决自动化下载需求
# 该爬虫写于2025.1.3至2025.1.5，随时间网站元素定位可能会变化，发现问题需自行修改
class PKULawSpider:
    # 初始化函数，打开北大法宝搜索界面
    def __init__(self, visible=True) -> None:
        chrome_driver_path = r"F:\python3.11\chromedriver.exe" # chromedriver自行填写
        options = Options()
        options.headless = not visible
        options.add_argument("--no-sandbox")
        options.add_argument('--ignore-certificate-errors')
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.pkulaw.com/case?way=topGuid")
        # 这里如果不设置全屏可能会引起错误，如无法点击搜索按钮
        self.driver.fullscreen_window()
        log("爬虫已启动！")
        sleep()
    def exit(self):
        self.driver.close()
        log("进程已结束！")
    def __find(self, by, addr):
        pass
    def __find_all(self, by, addr):
        pass
    def __tocsv(self, v: list, name: str):
        f = open(f'{name}.csv', mode='a', encoding='utf-8', newline='')

    def search(self,key: str):
        search = self.driver.find_element(By.ID, 'txtSearch')
        search.send_keys(key)
        sleep()
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSearch"]')))
        button.click()
    # 获取每一个案件的链接，默认爬取5页
    def get_links(self, end_page=5, print_=True, to_csv=True):
        # //*[@id="rightContent"]/div[3]/div[1]/div[2]/div[1]
        next_page_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[logfunc="翻页"]')))
        for _ in range(end_page):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep()
            cases = self.driver.find_elements(By.CLASS_NAME, 'item')
            cases_dict = dict()
            for case in cases:
                try:
                    name = case.find_element(By.XPATH, './/h4/a')
                    link = name.get_attribute('href')
                    title = name.text.strip()
                    if print_ and link and title:
                        print(f'{title},{link}')
                    cases_dict[title] = link
                except:
                    continue
            next_page_button.click()
        log(f"共读取{end_page}页")
        return cases_dict

# 实现打开单个链接读取判决内容
class CaseReader:
    def __init__(self) -> None:
        self.casePath = r""



if __name__ == '__main__':

    spider = PKULawSpider()
    spider.search('侵权')
    spider.get_links()
    spider.exit()