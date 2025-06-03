#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器操作引擎
封装 Selenium 的基础操作，提供统一的浏览器自动化接口
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os


class BrowserEngine:
    """浏览器操作引擎"""

    def __init__(self, headless: bool = False, timeout: int = 10):
        """
        初始化浏览器引擎

        Args:
            headless: 是否无头模式运行
            timeout: 默认等待超时时间（秒）
        """
        self.driver = None
        self.wait = None
        self.timeout = timeout
        self.headless = headless

    def start_browser(self, user_data_dir: str = None):
        """
        启动浏览器

        Args:
            user_data_dir: Chrome用户数据目录，用于保持登录状态
        """
        try:
            # Chrome选项设置
            chrome_options = Options()

            if self.headless:
                chrome_options.add_argument('--headless')

            # 常用设置
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # 如果指定了用户数据目录，使用它来保持登录状态
            if user_data_dir:
                chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

            # 启动浏览器
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, self.timeout)

            print("[浏览器] 启动成功")
            return True

        except Exception as e:
            print(f"[错误] 启动浏览器失败: {e}")
            print("请确保已安装 Chrome 浏览器和 ChromeDriver")
            return False

    def navigate_to(self, url: str) -> bool:
        """
        导航到指定URL

        Args:
            url: 目标URL

        Returns:
            bool: 是否成功
        """
        try:
            self.driver.get(url)
            print(f"[导航] 已访问: {url}")
            return True
        except Exception as e:
            print(f"[错误] 导航失败: {e}")
            return False

    def find_element_safe(self, selector: str, by: By = By.CSS_SELECTOR):
        """
        安全地查找元素

        Args:
            selector: 选择器
            by: 查找方式，默认CSS选择器

        Returns:
            WebElement 或 None
        """
        try:
            element = self.wait.until(EC.presence_of_element_located((by, selector)))
            return element
        except TimeoutException:
            print(f"[警告] 未找到元素: {selector}")
            return None

    def find_and_fill(self, selector: str, value: str, by: By = By.CSS_SELECTOR) -> bool:
        """
        查找元素并填入值

        Args:
            selector: 选择器
            value: 要填入的值
            by: 查找方式，默认CSS选择器

        Returns:
            bool: 是否成功
        """
        try:
            element = self.find_element_safe(selector, by)
            if element:
                # 清空现有内容
                element.clear()
                # 填入新值
                element.send_keys(value)
                print(f"[填充] {selector} = {value}")
                return True
            return False
        except Exception as e:
            print(f"[错误] 填充失败 {selector}: {e}")
            return False

    def find_and_click(self, selector: str, by: By = By.CSS_SELECTOR) -> bool:
        """
        查找元素并点击

        Args:
            selector: 选择器
            by: 查找方式，默认CSS选择器

        Returns:
            bool: 是否成功
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, selector)))
            element.click()
            print(f"[点击] {selector}")
            return True
        except TimeoutException:
            print(f"[警告] 元素不可点击: {selector}")
            return False
        except Exception as e:
            print(f"[错误] 点击失败 {selector}: {e}")
            return False

    def select_dropdown(self, selector: str, value: str, by: By = By.CSS_SELECTOR) -> bool:
        """
        选择下拉框选项

        Args:
            selector: 下拉框选择器
            value: 要选择的值
            by: 查找方式，默认CSS选择器

        Returns:
            bool: 是否成功
        """
        try:
            element = self.find_element_safe(selector, by)
            if element:
                select = Select(element)
                try:
                    select.select_by_visible_text(value)
                except:
                    select.select_by_value(value)
                print(f"[选择] {selector} = {value}")
                return True
            return False
        except Exception as e:
            print(f"[错误] 下拉选择失败 {selector}: {e}")
            return False

    def wait_for_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = None):
        """
        等待元素出现

        Args:
            selector: 选择器
            by: 查找方式
            timeout: 超时时间，默认使用初始化时的timeout

        Returns:
            WebElement 或 None
        """
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located((by, selector)))
            return element
        except TimeoutException:
            print(f"[超时] 等待元素超时: {selector}")
            return None

    def scroll_to_element(self, selector: str, by: By = By.CSS_SELECTOR) -> bool:
        """
        滚动到指定元素

        Args:
            selector: 选择器
            by: 查找方式

        Returns:
            bool: 是否成功
        """
        try:
            element = self.find_element_safe(selector, by)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(0.5)  # 等待滚动完成
                return True
            return False
        except Exception as e:
            print(f"[错误] 滚动失败 {selector}: {e}")
            return False

    def take_screenshot(self, filename: str = None) -> str:
        """
        截图

        Args:
            filename: 文件名，不指定则自动生成

        Returns:
            str: 截图文件路径
        """
        if not filename:
            filename = f"screenshot_{int(time.time())}.png"

        try:
            self.driver.save_screenshot(filename)
            print(f"[截图] 已保存: {filename}")
            return filename
        except Exception as e:
            print(f"[错误] 截图失败: {e}")
            return None

    def wait_seconds(self, seconds: int):
        """
        等待指定秒数

        Args:
            seconds: 等待时间（秒）
        """
        print(f"[等待] {seconds} 秒...")
        time.sleep(seconds)

    def get_current_url(self) -> str:
        """获取当前页面URL"""
        try:
            return self.driver.current_url
        except:
            return ""

    def get_page_title(self) -> str:
        """获取页面标题"""
        try:
            return self.driver.title
        except:
            return ""

    def close_browser(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("[浏览器] 已关闭")

    def __enter__(self):
        """支持 with 语句"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持 with 语句，自动关闭浏览器"""
        self.close_browser()


# 便捷函数
def create_browser(headless: bool = False, timeout: int = 10) -> BrowserEngine:
    """
    创建浏览器引擎实例

    Args:
        headless: 是否无头模式
        timeout: 默认超时时间

    Returns:
        BrowserEngine: 浏览器引擎实例
    """
    return BrowserEngine(headless=headless, timeout=timeout)


if __name__ == "__main__":
    # 测试代码
    print("=== 浏览器引擎测试 ===")

    with create_browser() as browser:
        if browser.start_browser():
            # 测试导航
            browser.navigate_to("https://www.baidu.com")
            browser.wait_seconds(2)

            # 测试填充搜索框
            browser.find_and_fill("#kw", "Python自动化")
            browser.wait_seconds(1)

            # 测试点击搜索按钮
            browser.find_and_click("#su")
            browser.wait_seconds(3)

            print("测试完成")