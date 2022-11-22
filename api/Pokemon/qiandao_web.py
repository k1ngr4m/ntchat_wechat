import json
import random
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import urllib.request
import os

import urllib.request

class QiandaoWeb:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(r'--user-data-dir=C:\ChromeUserData')

        # 2> 添加无头参数r,一定要使用无头模式，不然截不了全页面，只能截到你电脑的高度
        chrome_options.add_argument('--headless')
        # 3> 为了解决一些莫名其妙的问题关闭 GPU 计算
        chrome_options.add_argument('--disable-gpu')
        # 4> 为了解决一些莫名其妙的问题浏览器不动
        chrome_options.add_argument('--no-sandbox')

        # 开启开发者工具（F12）
        # chrome_options.add_argument("--auto-open-devtools-for-tabs")
        chrome_options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone 12 Pro'})
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver = webdriver.Chrome()

        self.driver.get('https://m.qiandaoapp.com/plugin/pokedex?pkg=1000')
        time.sleep(1)
        self.driver.maximize_window()

        self.search_box = self.driver.find_element(By.CLASS_NAME, 'searchbox')

    def search_pokemon_main(self, name):
        self.search_pokemon_by_name(name)
        png_path = self.screenshot_main(name)
        self.driver.close()
        return png_path

    def search_pokemon_catch(self, name):
        self.search_pokemon_by_name(name)
        png_path = self.screenshot_catch(name)
        self.driver.close()
        return png_path

    def search_pokemon_by_name(self, name):
        try:
            time.sleep(1)
            self.search_box.send_keys(name)
            time.sleep(1)
            self.search_box.send_keys(' ')

            time.sleep(1)
            self.driver.find_element(By.XPATH, "//li[starts-with(@class, 'item')]").click()
            time.sleep(1)
        except Exception as e:
            print(e)

    def screenshot_main(self, name):
        try:
            # time.sleep(1)
            width = self.driver.execute_script(
                "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
                "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
                "document.documentElement.offsetWidth);")
            height = self.driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
                "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
                "document.documentElement.offsetHeight);")
            print(width, height)

            self.driver.set_window_size(width + 500, height + 400)

            pngs_path = rf'C:\py\git\PythonProject\ntchat_wechat\data\pokemon'
            path = rf'C:\py\git\PythonProject\ntchat_wechat\data\pokemon\temp'

            detail_info = self.driver.find_element(By.CLASS_NAME, 'detail-info')

            detail_header = detail_info.find_element(By.XPATH, '//*[@class="detail-info"]/div[1]')
            img_1 = path + fr'\{name}_detail_header.png'
            detail_header.screenshot(path + fr'\{name}_detail_header.png')

            ability = detail_info.find_element(By.XPATH, '//*[@class="detail-info"]/div[3]')
            img_2 = path + fr'\{name}_ability.png'
            ability.screenshot(path + fr'\{name}_ability.png')

            egg = detail_info.find_element(By.XPATH, '//*[@class="detail-info"]/div[4]')
            img_3 = path + fr'\{name}_egg.png'
            egg.screenshot(path + fr'\{name}_egg.png')

            else_info = detail_info.find_element(By.XPATH, '//*[@class="detail-info"]/div[5]')
            if else_info.size['height'] != 0:
                print(else_info.size)
                img_4 = path + fr'\{name}_else_info.png'
                else_info.screenshot(path + fr'\{name}_else_info.png')
            else:
                img_4 = r'C:\py\git\PythonProject\ntchat_wechat\data\pokemon\temp\temp.png'

            species_strength = detail_info.find_element(By.XPATH, '//*[@class="detail-info"]/ul')
            img_5 = path + fr'\{name}_species_strength.png'
            species_strength.screenshot(path + fr'\{name}_species_strength.png')

            # self.roll_window_to_bottom(self.driver)

            attribute_restraint = detail_info.find_element(By.XPATH, '//*[@class="detail-info"]/div[6]')
            img_6 = path + fr'\{name}_attribute_restraint.png'
            attribute_restraint.screenshot(path + fr'\{name}_attribute_restraint.png')

            evolutionary_links = detail_info.find_element(By.XPATH, '//*[@class="detail-info"]/div[7]')
            img_7 = path + fr'\{name}_evolutionary_links.png'
            evolutionary_links.screenshot(path + fr'\{name}_evolutionary_links.png')

            # self.driver.close()
            # png.screenshot(path)
            print('success')
            png_path = self.image_Splicing(img_1, img_2, img_3, img_4, img_5, img_6, img_7, pngs_path, name)
            return png_path
        except Exception as e:
            print(e)

    def screenshot_catch(self, name):
        self.driver.find_element(By.XPATH, "//span[text()=' 捕捉地点 ']").click()

        # availability_group = self.driver.find_element(By.CLASS_NAME, 'availability-group')
        info = self.driver.find_element(By.XPATH, '//*[@class="availability-group"]/div[1]')
        info1 = self.driver.find_element(By.XPATH, '//*[@class="availability-group"]/div[1]/div[1]')
        info_title = info1.text
        print(info_title)
        if info_title == '朱紫':
            img = info.find_element(By.TAG_NAME, 'img')
            src_url = img.get_attribute('src')
            # print(src)
            file_name = self.pic(src_url, name)
            return file_name
        else:
            return False

    def image_Splicing(self, img_1, img_2, img_3, img_4, img_5, img_6, img_7, path, name, flag='y'):
        print(f"开始拼图{name}")
        img1 = Image.open(img_1)
        img2 = Image.open(img_2)
        img3 = Image.open(img_3)
        img4 = Image.open(img_4)
        img5 = Image.open(img_5)
        img6 = Image.open(img_6)
        img7 = Image.open(img_7)
        size1, size2, size3, size4, size5, size6, size7 = img1.size, img2.size, img3.size, img4.size, img5.size, img6.size, img7.size

        # if flag == 'x':
        #     joint = Image.new("RGB", (size1[0] + size2[0], size1[1]))
        #     loc1, loc2 = (0, 0), (size1[0], 0)
        # else:
        joint = Image.new("RGB", (size1[0], size2[1] + size1[1] + size3[1] + size4[1] + size5[1] + size6[1] + size7[1]),
                          "white")
        loc1, loc2, loc3 = (0, 0), (50, size1[1]), (0, size1[1] + size2[1])
        loc4, loc5, loc6 = (0, loc3[1] + size3[1]), (0, loc3[1] + size3[1] + size4[1]), (
            0, loc3[1] + size3[1] + size4[1] + size5[1])
        loc7 = (0, loc6[1] + size6[1])

        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        joint.paste(img3, loc3)
        joint.paste(img4, loc4)
        joint.paste(img5, loc5)
        joint.paste(img6, loc6)
        joint.paste(img7, loc7)

        png_path = path + '/{}.png'.format(name)

        joint.save(png_path)
        print(f"{name}拼图成功！")
        return png_path

    def roll_window_to_bottom(self, browser, stop_length=None, step_length=500):
        """selenium 滚动当前页面，向下滑
        :param browser: selenium的webdriver
        :param stop_length: 滑动的最大值
        :param step_length: 每次滑动的值
        """
        original_top = 0
        while True:  # 循环向下滑动
            if stop_length:
                if stop_length - step_length < 0:
                    browser.execute_script("window.scrollBy(0,{})".format(stop_length))
                    break
                stop_length -= step_length

            browser.execute_script("window.scrollBy(0,{})".format(step_length))
            time.sleep(0.5 + random.random())  # 停顿一下
            check_height = browser.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            if check_height == original_top:  # 判断滑动后距顶部的距离与滑动前距顶部的距离
                break
            original_top = check_height

    # 图片转换成文件
    def pic(self, url, pic_name):
        img_url = url
        file_path = rf'C:\py\git\PythonProject\ntchat_wechat\data\pokemon'
        file_name = pic_name + '_catch'
        try:
            # 是否有这个路径
            if not os.path.exists(file_path):
                # 创建路径
                os.makedirs(file_path)
            # 获得图片后缀
            file_suffix = os.path.splitext(img_url)[1]
            print(file_suffix)
            # 拼接图片名（包含路径）
            filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
            print(filename)
            opener = urllib.request.build_opener()
            opener.addheaders = [(
                'User-Agent',
                'Mozilla / 5.0 (Windows NT 6.1; WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                '36.0.1941.0Safari / 537.36 '
            )]
            urllib.request.install_opener(opener)
            # 下载图片，并保存到文件夹中
            urllib.request.urlretrieve(img_url, filename=filename)
            return filename
        except IOError as e:
            print(f"IOError:{e}")
        except Exception as e:
            print("Exception")


if __name__ == '__main__':
    qdweb = QiandaoWeb()
    qdweb.search_pokemon_catch('小火龙')
