# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   MfyPublic
# FileName:     base
# Author:      MingFeiyang
# Datetime:    2021/8/3 15:40
# -----------------------------------------------------------------------------------
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Base:

    def __init__(self, browser,url):
        """
        选择浏览器，并最大化浏览器，并打开测试网址
        :param browser: 浏览器类型，这里只做了Chrome，Firefox，Ie三个浏览器
        :param url: 测试的网址
        """
        if browser == "c" or browser == "C" or browser == "Chrome":
            self.driver = webdriver.Chrome()
        elif browser == "f" or browser == "F" or browser == "Firefox":
            self.driver = webdriver.Firefox()
        elif browser == "i" or browser == "I" or browser == "Ie":
            self.driver = webdriver.Ie()
        else:
            raise NameError("请输入正确的浏览器参数！！！")
        # 最大化浏览器窗口
        self.driver.maximize_window()
        # 输入网址
        self.driver.get(url)

    def implicitly_wait(self, time_to_wait):
        """
        隐式等待
        :param time_to_wait:等待的时间
        :return:
        """
        self.driver.implicitly_wait(time_to_wait)

    def _location_element(self, location, value, num="dan"):
        """
        定位元素
        :param location:定位方法
        :param value: 定位方法所对应的值
        :param num: 当num="dan" ,返回的是单个元素定位，其他值，为复数
        :return: 定位到的元素
        """
        if location == "i":
            locator = (By.ID, value)
        elif location == "n":
            locator = (By.NAME, value)
        elif location == "c":
            locator = (By.CLASS_NAME, value)
        elif location == "x":
            locator = (By.XPATH, value)
        elif location == "t":
            locator = (By.TAG_NAME, value)
        elif location == "l":
            locator = (By.LINK_TEXT, value)
        elif location == "p":
            locator = (By.PARTIAL_LINK_TEXT, value)
        elif location == "s":
            locator = (By.CSS_SELECTOR, value)
        else:
            raise NameError("请输入正确的定位方式！！！")
        if num == "dan":
            return WebDriverWait(self.driver, 20, 1).until(ec.presence_of_element_located(locator))
        else:
            return WebDriverWait(self.driver, 20, 1).until(ec.presence_of_all_elements_located(locator))

    def send_keys(self, location, value, text):
        """
        对定位到的元素输入内容
        :param location: 定位的方法
        :param value: 定位方法所对应的值
        :param text: 需要输入的文本
        :return:
        """
        ele = self._location_element(location, value)
        ele.clear()
        ele.send_keys(text)

    def click(self, location, value):
        """
        对定位到的元素进行点击
        :param location: 定位方法
        :param value: 定位方法所对应的值
        :return:
        """
        self._location_element(location, value).click()

    def switch_to_frame(self, location, value):
        """
        进入iframe框架
        :param location:定位方法
        :param value: 定位方法所对应的值
        :return:
        """
        ele = self._location_element(location, value)
        self.driver.switch_to.frame(ele)

    def switch_to_default_content(self):
        """
        退出到iframe框架最外层
        :return:
        """
        self.driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        """
        退出到iframe框架上一层
        :return:
        """
        self.driver.switch_to.parent_frame()

    def random_choice(self, location, value):
        """
        随机选择性别
        :param location: 定位方法
        :param value: 定位方法所对应的值
        :return:
        """
        eles = self._location_element(location, value, num="shuang")
        random.choice(eles).click()

    def select_by_index(self, location, value, num):
        """
        select下拉框，通过索引定位
        :param location: 定位方法
        :param value: 定位方法所对应的值
        :param num: 索引
        :return:
        """
        ele = self._location_element(location, value)
        Select(ele).select_by_index(num)

    def select_by_value(self, location, value, value1):
        """
        select下拉框，通过value定位
        :param location: 定位方法
        :param value: 定位方法所对应的值
        :param value1: value值
        :return:
        """
        ele = self._location_element(location, value)
        Select(ele).select_by_value(value1)

    def select_by_visible_text(self, location, value, text):
        """
        select下拉框，通过文本定位
        :param location: 定位方法
        :param value: 定位方法所对应的值
        :param text: 文本值
        :return:
        """
        ele = self._location_element(location, value)
        Select(ele).select_by_visible_text(text)

    def twice_element(self, by1=By.ID, value1=None, by2=By.TAG_NAME, value2=None):
        """
        二次定位，可以实现对元素集合进行随机点击
        :param by1: 父级的定位方法
        :param value1: 父级的定位方法所对应的值
        :param by2: 子级的定位方法
        :param value2: 子级的定位方法所对应的值
        :return:
        """
        ele = self.driver.find_element(by1, value1).find_elements(by2, value2)
        random.choice(ele).click()

    def get_text(self, location, value):
        """
        获取单个文本
        :param location: 定位方法
        :param value: 定位方法所对应的值
        :return: 获取到的文本
        """
        return self._location_element(location, value).text

    def get_texts(self, location, value):
        """
        获取多个文本
        :param location: 定位方法
        :param value: 定位方法所对应的值
        :return:
        """
        eles = self._location_element(location, value, num="shuang")
        texts = []
        for ele in eles:
            text = ele.text
            texts.append(text)
        return texts

    def quit(self):
        """
        杀浏览器进程
        :return:
        """
        self.driver.quit()

    def close(self):
        """
        关闭浏览器窗口
        :return:
        """
        self.driver.close()

    def save_screenshot(self,filename):
        """
        保存截图，格式是png
        :param filename: 截图保存的路径
        :return:
        """
        self.driver.save_screenshot(filename)

    def get_screenshot_as_file(self,filename):
        """
        保存截图，格式是png
        :param filename: 截图保存的路径
        :return:
        """
        self.driver.get_screenshot_as_file(filename)

