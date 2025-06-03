#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块 - 项目的记忆核心
实现智能的"问答式"配置管理，按需补充用户信息
"""

import configparser
import os
from typing import Optional


class ConfigManager:
    """配置管理器 - 实现读写和按需补充功能"""

    def __init__(self, config_file: str = "config.ini"):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径，默认为 config.ini
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            self._create_default_config()

    def _create_default_config(self):
        """创建默认的配置文件"""
        # 基础个人信息
        self.config.add_section('PersonalInfo')
        self.config.set('PersonalInfo', 'name', '张三')
        self.config.set('PersonalInfo', 'phone', '13800138000')
        self.config.set('PersonalInfo', 'email', 'zhangsan@example.com')

        # 工作相关信息（空白，等待用户填充）
        self.config.add_section('WorkInfo')

        # 教育背景（空白，等待用户填充）
        self.config.add_section('Education')

        # 其他信息
        self.config.add_section('Others')

        self._save_config()
        print(f"[初始化] 已创建默认配置文件: {self.config_file}")

    def _save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            print(f"[错误] 保存配置文件失败: {e}")

    def _write_to_config(self, section: str, key: str, value: str):
        """
        写入新的配置项到配置文件

        Args:
            section: 配置节名
            key: 配置键名
            value: 配置值
        """
        # 确保节存在
        if not self.config.has_section(section):
            self.config.add_section(section)

        # 设置值并保存
        self.config.set(section, key, value)
        self._save_config()
        print(f"[保存] {section}.{key} = {value}")

    def get_or_ask(self, section: str, key: str, prompt_text: str) -> str:
        """
        核心函数：获取配置值，如果不存在则询问用户并保存

        Args:
            section: 配置节名
            key: 配置键名
            prompt_text: 当配置不存在时向用户显示的提示文本

        Returns:
            str: 配置值（从文件读取或用户输入）
        """
        try:
            # 尝试从配置文件读取
            value = self.config.get(section, key)
            if value and value.strip():  # 检查值是否非空
                print(f"[读取] {section}.{key} = {value}")
                return value
            else:
                # 值为空，需要询问用户
                raise configparser.NoOptionError(key, section)

        except (configparser.NoSectionError, configparser.NoOptionError):
            # 配置不存在，询问用户
            print(f"\n{prompt_text}")
            user_input = input("请输入: ").strip()

            # 如果用户输入为空，再次询问
            while not user_input:
                print("输入不能为空，请重新输入:")
                user_input = input("请输入: ").strip()

            # 保存用户输入到配置文件
            self._write_to_config(section, key, user_input)
            return user_input

    def get_config_value(self, section: str, key: str, default: str = "") -> str:
        """
        直接获取配置值，不询问用户

        Args:
            section: 配置节名
            key: 配置键名
            default: 默认值

        Returns:
            str: 配置值或默认值
        """
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def set_config_value(self, section: str, key: str, value: str):
        """
        直接设置配置值

        Args:
            section: 配置节名
            key: 配置键名
            value: 配置值
        """
        self._write_to_config(section, key, value)

    def show_all_config(self):
        """显示所有配置信息"""
        print("\n=== 当前配置信息 ===")
        for section_name in self.config.sections():
            print(f"\n[{section_name}]")
            for key, value in self.config.items(section_name):
                print(f"{key} = {value}")
        print("==================\n")


# 创建全局配置管理器实例
_config_manager = ConfigManager()


# 提供便捷的函数接口
def get_or_ask(section: str, key: str, prompt_text: str) -> str:
    """
    便捷函数：获取配置值，如果不存在则询问用户并保存

    Args:
        section: 配置节名
        key: 配置键名
        prompt_text: 提示文本

    Returns:
        str: 配置值
    """
    return _config_manager.get_or_ask(section, key, prompt_text)


def get_config(section: str, key: str, default: str = "") -> str:
    """
    便捷函数：直接获取配置值

    Args:
        section: 配置节名
        key: 配置键名
        default: 默认值

    Returns:
        str: 配置值或默认值
    """
    return _config_manager.get_config_value(section, key, default)


def set_config(section: str, key: str, value: str):
    """
    便捷函数：设置配置值

    Args:
        section: 配置节名
        key: 配置键名
        value: 配置值
    """
    _config_manager.set_config_value(section, key, value)


def show_config():
    """便捷函数：显示所有配置"""
    _config_manager.show_all_config()


if __name__ == "__main__":
    # 测试代码
    print("=== 配置管理器测试 ===")

    # 测试获取现有配置
    name = get_or_ask('PersonalInfo', 'name', '[测试] 请输入姓名:')
    print(f"获取到姓名: {name}")

    # 测试获取不存在的配置（会询问用户）
    salary = get_or_ask('WorkInfo', 'expected_salary', '[测试] 请输入期望薪资:')
    print(f"获取到期望薪资: {salary}")

    # 显示所有配置
    show_config()