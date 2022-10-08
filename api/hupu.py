import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Hupu:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(r'--user-data-dir=C:\ChromeUserData')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)


    def autologin(self):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(r'--user-data-dir=D:\ChromeUserData')
        # driver = webdriver.Chrome(options=chrome_options)
        try:
            self.driver.get('https://my.hupu.com/35904121053081')
            time.sleep(10)
            self.driver.find_element(By.XPATH, '//input[@placeholder="账号"]').send_keys('你科年轻美如画')
            self.driver.find_element(By.XPATH, '//input[@placeholder="密码"]').send_keys('ColayKD41')
            self.driver.find_element(By.XPATH, '//div[@id="rectMask"]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//span[text()="登 录"]').click()
            time.sleep(1)
            print('cookies is saved')
        except Exception as e:
            print(e)

    def get_report(self):
        self.driver.get('https://my.hupu.com/35904121053081')
        time.sleep(1)
        lists = self.driver.find_elements(By.XPATH, '//*[contains(text(), "[赛后")]')
        lists[0].click()
        time.sleep(1)

        handles = self.driver.window_handles  # 获取当前浏览器的所有窗口句柄

        self.driver.switch_to.window(handles[-1])  # 切换到最新打开的窗口
        name = self.driver.find_element(By.XPATH, '//*[@class="name"]').text
        print('title got')
        self.driver.quit()
        return name

    def contrast(self, title):
        with open(r'data/hupu_title.txt', 'r', encoding='utf-8') as f:
            temp = f.read()
            print(temp)
            if title != temp:
                with open(r'data/hupu_title.txt', 'w', encoding='utf-8') as fs:
                    fs.write(title)
                    print('title changed')
                    return True
            else:
                return False

    def send_hupu_msg(self):
        title = self.get_report()
        res = self.contrast(title)
        if res:
            with open('hupu_title.txt', 'r', encoding='utf-8') as f:
                title = f.read()
            # send title
            print(title)
