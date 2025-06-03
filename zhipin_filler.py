#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS直聘信息填充脚本
针对BOSS直聘网站的个人简历信息自动填充
"""

import config_manager
import browser_engine
from selenium.webdriver.common.by import By
import time


class ZhipinFiller:
    """BOSS直聘信息填充器"""

    def __init__(self):
        """初始化填充器"""
        self.browser = browser_engine.create_browser(headless=False, timeout=15)
        self.base_url = "https://www.zhipin.com"

    def start_filling_process(self):
        """开始填充流程"""
        print("=== BOSS直聘简历信息自动填充 ===\n")

        try:
            # 启动浏览器
            if not self.browser.start_browser():
                return False

            # 导航到BOSS直聘
            print("请按以下步骤操作：")
            print("1. 浏览器将打开BOSS直聘网站")
            print("2. 请手动登录您的账户")
            print("3. 登录后，请导航到简历编辑页面")
            print("4. 准备好后，按回车键继续自动填充...")

            self.browser.navigate_to(self.base_url)

            # 等待用户手动登录并导航到简历页面
            input("\n请完成登录并进入简历编辑页面，然后按回车继续...")

            # 开始填充个人信息
            self._fill_personal_info()

            # 填充工作相关信息
            self._fill_work_info()

            # 填充教育背景
            self._fill_education_info()

            # 填充其他信息
            self._fill_other_info()

            print("\n=== 填充完成 ===")
            print("请检查填充结果，如需修改可直接在页面上编辑")
            input("按回车键关闭浏览器...")

            return True

        except Exception as e:
            print(f"[错误] 填充过程出现异常: {e}")
            return False
        finally:
            self.browser.close_browser()

    def _fill_personal_info(self):
        """填充个人基础信息"""
        print("\n--- 填充个人基础信息 ---")

        # 常见的个人信息字段选择器（需要根据实际页面调整）
        fields = [
            {
                'selector': 'input[name="name"], input[placeholder*="姓名"], input[placeholder*="真实姓名"]',
                'config_section': 'PersonalInfo',
                'config_key': 'name',
                'prompt': '[个人信息] 请输入您的真实姓名:'
            },
            {
                'selector': 'input[name="mobile"], input[placeholder*="手机"], input[placeholder*="电话"]',
                'config_section': 'PersonalInfo',
                'config_key': 'phone',
                'prompt': '[个人信息] 请输入您的手机号码:'
            },
            {
                'selector': 'input[name="email"], input[placeholder*="邮箱"], input[type="email"]',
                'config_section': 'PersonalInfo',
                'config_key': 'email',
                'prompt': '[个人信息] 请输入您的邮箱地址:'
            },
            {
                'selector': 'input[name="age"], input[placeholder*="年龄"]',
                'config_section': 'PersonalInfo',
                'config_key': 'age',
                'prompt': '[个人信息] 请输入您的年龄:'
            },
            {
                'selector': 'input[name="address"], input[placeholder*="地址"], input[placeholder*="现居"]',
                'config_section': 'PersonalInfo',
                'config_key': 'address',
                'prompt': '[个人信息] 请输入您的现居地址:'
            }
        ]

        for field in fields:
            self._fill_field_safe(field)

    def _fill_work_info(self):
        """填充工作相关信息"""
        print("\n--- 填充工作相关信息 ---")

        fields = [
            {
                'selector': 'input[name="expectedSalary"], input[placeholder*="期望薪资"], input[placeholder*="薪资"]',
                'config_section': 'WorkInfo',
                'config_key': 'expected_salary',
                'prompt': '[工作信息] 请输入您的期望薪资 (如: 15k-25k):'
            },
            {
                'selector': 'input[name="jobTitle"], input[placeholder*="职位"], input[placeholder*="岗位"]',
                'config_section': 'WorkInfo',
                'config_key': 'desired_position',
                'prompt': '[工作信息] 请输入您的期望职位:'
            },
            {
                'selector': 'input[name="workExperience"], input[placeholder*="工作经验"], input[placeholder*="经验"]',
                'config_section': 'WorkInfo',
                'config_key': 'work_experience',
                'prompt': '[工作信息] 请输入您的工作经验 (如: 3年):'
            },
            {
                'selector': 'textarea[name="selfIntroduction"], textarea[placeholder*="自我介绍"], textarea[placeholder*="个人描述"]',
                'config_section': 'WorkInfo',
                'config_key': 'self_introduction',
                'prompt': '[工作信息] 请输入您的自我介绍:'
            }
        ]

        for field in fields:
            self._fill_field_safe(field)

    def _fill_education_info(self):
        """填充教育背景信息"""
        print("\n--- 填充教育背景信息 ---")

        fields = [
            {
                'selector': 'input[name="school"], input[placeholder*="学校"], input[placeholder*="院校"]',
                'config_section': 'Education',
                'config_key': 'school_name',
                'prompt': '[教育背景] 请输入您的毕业院校:'
            },
            {
                'selector': 'input[name="major"], input[placeholder*="专业"]',
                'config_section': 'Education',
                'config_key': 'major',
                'prompt': '[教育背景] 请输入您的专业:'
            },
            {
                'selector': 'input[name="degree"], input[placeholder*="学历"]',
                'config_section': 'Education',
                'config_key': 'degree',
                'prompt': '[教育背景] 请输入您的学历 (如: 本科/硕士/博士):'
            },
            {
                'selector': 'input[name="graduationYear"], input[placeholder*="毕业时间"], input[placeholder*="毕业年份"]',
                'config_section': 'Education',
                'config_key': 'graduation_year',
                'prompt': '[教育背景] 请输入您的毕业年份 (如: 2020):'
            }
        ]

        for field in fields:
            self._fill_field_safe(field)

    def _fill_other_info(self):
        """填充其他信息"""
        print("\n--- 填充其他信息 ---")

        fields = [
            {
                'selector': 'textarea[name="projectExperience"], textarea[placeholder*="项目经验"]',
                'config_section': 'Others',
                'config_key': 'project_experience',
                'prompt': '[其他信息] 请输入您的项目经验:'
            },
            {
                'selector': 'textarea[name="skills"], textarea[placeholder*="技能"], textarea[placeholder*="专业技能"]',
                'config_section': 'Others',
                'config_key': 'professional_skills',
                'prompt': '[其他信息] 请输入您的专业技能:'
            },
            {
                'selector': 'input[name="github"], input[placeholder*="GitHub"], input[placeholder*="github"]',
                'config_section': 'Others',
                'config_key': 'github_url',
                'prompt': '[其他信息] 请输入您的GitHub地址 (可选，直接回车跳过):'
            }
        ]

        for field in fields:
            self._fill_field_safe(field, required=False)

    def _fill_field_safe(self, field_config: dict, required: bool = True):
        """
        安全地填充字段

        Args:
            field_config: 字段配置字典
            required: 是否必填字段
        """
        selector = field_config['selector']
        config_section = field_config['config_section']
        config_key = field_config['config_key']
        prompt = field_config['prompt']

        try:
            # 尝试找到元素
            element = self.browser.find_element_safe(selector)

            if element:
                # 获取配置值（可能会询问用户）
                if required:
                    value = config_manager.get_or_ask(config_section, config_key, prompt)
                else:
                    # 非必填字段，允许空值
                    try:
                        value = config_manager.get_config(config_section, config_key)
                        if not value:
                            print(f"{prompt}")
                            user_input = input("请输入 (可选，直接回车跳过): ").strip()
                            if user_input:
                                config_manager.set_config(config_section, config_key, user_input)
                                value = user_input
                    except:
                        print(f"{prompt}")
                        user_input = input("请输入 (可选，直接回车跳过): ").strip()
                        if user_input:
                            config_manager.set_config(config_section, config_key, user_input)
                            value = user_input
                        else:
                            value = ""

                # 如果有值则填充
                if value:
                    success = self.browser.find_and_fill(selector, value)
                    if success:
                        # 填充成功后稍等一下
                        time.sleep(0.5)
                    else:
                        print(f"[跳过] 无法填充字段: {config_key}")
                else:
                    print(f"[跳过] 字段为空: {config_key}")
            else:
                print(f"[跳过] 未找到字段: {config_key}")

        except Exception as e:
            print(f"[错误] 填充字段失败 {config_key}: {e}")

    def _try_multiple_selectors(self, selectors: list) -> str:
        """
        尝试多个选择器，返回第一个找到的

        Args:
            selectors: 选择器列表

        Returns:
            str: 找到的选择器，或空字符串
        """
        for selector in selectors:
            element = self.browser.find_element_safe(selector)
            if element:
                return selector
        return ""

    def fill_specific_page(self, page_url: str):
        """
        填充指定页面

        Args:
            page_url: 页面URL
        """
        print(f"导航到指定页面: {page_url}")
        if self.browser.navigate_to(page_url):
            time.sleep(2)  # 等待页面加载
            self._fill_personal_info()
            self._fill_work_info()
            self._fill_education_info()
            self._fill_other_info()


def main():
    """主函数"""
    filler = ZhipinFiller()
    filler.start_filling_process()


if __name__ == "__main__":
    main()