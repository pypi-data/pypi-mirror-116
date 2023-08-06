# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   MfyPublic
# FileName:     base
# Author:      MingFeiyang
# Datetime:    2021-05-18 15:42
# -----------------------------------------------------------------------------------
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base:

    def __init__(self, browser, url):
        """
        选择浏览器，并最大化浏览器，并打开测试网址
        :param browser: 浏览器类型，这里只做了Chrome，Firefox，Ie三个浏览器
        :param url: 测试的网址
        """
        if browser == "Chrome" or browser == "c" or browser == "C":
            self.driver = webdriver.Chrome()  # 实例化谷歌浏览器并打开
        elif browser == "f" or browser == "F" or browser == "Firefox":
            self.driver = webdriver.Firefox()  # 实例化火狐浏览器并打开
        elif browser == "i" or browser == "I" or browser == "Ie":
            self.driver = webdriver.Ie()
        else:
            raise NameError("请输入正确的浏览器类型！！！")
        # 最大化浏览器
        self.driver.maximize_window()
        # 打开网址
        self.driver.get(url)

    def implicitly_wait(self, time_to_wait):
        """
        隐式等待
        :param time_to_wait:等待的时间
        :return:
        """
        self.driver.implicitly_wait(time_to_wait)

    def selector_to_locator(self, selector):
        """
        表示把selector("i,account") 转换成locator(By.ID，account)
        :param selector: selector("i,account")
        :return: locator
        """
        selector_by = selector.split(",")[0].strip()
        selector_value = selector.split(",")[1].strip()
        if selector_by == "i" or selector_by == "id":
            locator = (By.ID, selector_value)
        elif selector_by == "n" or selector_by == "name":
            locator = (By.NAME, selector_value)
        elif selector_by == "c" or selector_by == "class_name":
            locator = (By.CLASS_NAME, selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            locator = (By.XPATH, selector_value)
        elif selector_by == "l" or selector_by == "link_text":
            locator = (By.LINK_TEXT, selector_value)
        elif selector_by == "p" or selector_by == "partial_link_text":
            locator = (By.PARTIAL_LINK_TEXT, selector_value)
        elif selector_by == "t" or selector_by == "tag_name":
            locator = (By.TAG_NAME, selector_value)
        elif selector_by == "s" or selector_by == "css_selector":
            locator = (By.CSS_SELECTOR, selector_value)
        else:
            raise NameError("请输入正确的定位方式！！！")
        return locator  # (By.ID,"value")

    def _locator_element(self, selector):
        """
        定位元素
        :param selector:'i,account'
        :return: 返回定位到的元素
        """
        locator = self.selector_to_locator(selector)
        return WebDriverWait(self.driver, 20, 1).until(EC.presence_of_element_located(locator))

    def _locator_elements(self, selector):
        """
        定位多个元素
        :param selector:定位方式
        :return: 返回定位到的元素
        """
        locator = self.selector_to_locator(selector)
        return WebDriverWait(self.driver,20,1).until(EC.presence_of_all_elements_located(locator))


    def random_choice_click(self, selector):
        """
        从多个元素中随机选择一个进行点击
        :param selector:
        :return:
        """
        ele_list = self._locator_elements(selector)
        random.choice(ele_list).click()

    def send_keys(self, selector, text):
        """
        对定位到的元素进行，输入内容
        :param selector:（i,account）
        :param text: 输入的内容
        :return:
        """
        ele = self._locator_element(selector)
        ele.clear()
        ele.send_keys(text)

    def click(self, selector):
        """
        对定位到的元素进行点击
        :param selector:
        :return:
        """
        self._locator_element(selector).click()

    def switch_to_frame(self, selector):
        """
        进入iframe框架
        :param selector:
        :return:
        """
        ele = self._locator_element(selector)
        WebDriverWait(self.driver, 20, 1).until(EC.frame_to_be_available_and_switch_to_it(ele))
        # self.driver.switch_to.frame(ele)

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

    def select_by_value(self, selector, value):
        """
        通过value值定位
        :param selector:
        :param value:
        :return:
        """
        Select(self._locator_element(selector)).select_by_value(value)

    def select_by_visible_text(self, selector, text):
        """
        通过文本值定位
        :param selector:
        :param value:
        :return:
        """
        Select(self._locator_element(selector)).select_by_visible_text(text)

    def select_by_index(self, selector, index):
        """
        通过索引值定位
        :param selector:
        :param value:
        :return:
        """
        Select(self._locator_element(selector)).select_by_index(index)

    def second_ele(self, selector1, selector2):
        """
        二次定位
        :param selector1:
        :param selector2:
        :return:
        """
        locator1 = self.selector_to_locator(selector1)
        locator2 = self.selector_to_locator(selector2)
        ele_dept = self.driver.find_element(*locator1).find_elements(*locator2)
        random.choice(ele_dept).click()

    def get_text(self, selector):
        """
        获取文本
        :param selector:
        :return:
        """
        return self._locator_element(selector).text

    def get_texts(self, selector):
        """
        获取多个文本
        :param selector:
        :return:
        """
        eles = self._locator_elements(selector)
        list_text = []
        for ele in eles:
            list_text.append(ele.text)
        return list_text

    def quit(self):
        """
        退出浏览器进程
        :return:
        """
        self.driver.quit()

    def close(self):
        """
        关闭浏览器窗口
        :return:
        """
        self.driver.close()

    def get_screenshot_as_file(self, filename):
        """
        保存截图
        :param filename: 图片的路径
        :return:
        """
        self.driver.get_screenshot_as_file(filename)

    def save_screenshot(self,filename):
        """
        保存截图
        :param filename:
        :return:
        """
        self.driver.save_screenshot(filename)

