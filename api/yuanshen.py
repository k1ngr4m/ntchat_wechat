import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Yuanshen:
    def get_item(self):
        url = 'https://wiki.biligame.com/ys/%E9%A6%96%E9%A1%B5'
        chrome_options = Options()
        # 2> 添加无头参数r,一定要使用无头模式，不然截不了全页面，只能截到你电脑的高度
        chrome_options.add_argument('--headless')
        # 3> 为了解决一些莫名其妙的问题关闭 GPU 计算
        chrome_options.add_argument('--disable-gpu')
        # 4> 为了解决一些莫名其妙的问题浏览器不动
        chrome_options.add_argument('--no-sandbox')
        # 5> 添加驱动地址。 由于在函数内，设置参数chrome_options需要再导入
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        driver.maximize_window()
        time.sleep(1)
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
            "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
            "document.documentElement.offsetWidth);")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
            "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);")
        # print(width, height)
        # 将浏览器的宽高设置成刚刚获取的宽高
        driver.set_window_size(width + 400, height + 100)
        path = r'C:\py\git\PythonProject\ntchat_wechat\data\yuanshen_time_manage.png'

        png = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/div/div[3]/div[4]/div')
        png.screenshot(path)

        print('finished')
        return path

    def get_item_path(self):
        weekday = datetime.date.today().isoweekday()
        print(weekday)
        path = r'C:\py\git\PythonProject\ntchat_wechat\data\yuanshen'
        if weekday == 1 or weekday == 4:
            role_path = path + r'\role_1_4.png'
            weapon_path = path + r'\weapon_1_4.png'
        elif weekday == 2 or weekday == 5:
            role_path = path + r'\role_2_5.png'
            weapon_path = path + r'\weapon_2_5.png'
        elif weekday == 3 or weekday == 6:
            role_path = path + r'\role_3_6.png'
            weapon_path = path + r'\weapon_3_6.png'
        else:
            role_path = path + r'\role_all.png'
            weapon_path = path + r'\weapon_all.png'
        print(role_path, weapon_path)
        return role_path, weapon_path


if __name__ == '__main__':
    Yuanshen().get_item_path()