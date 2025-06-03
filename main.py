#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动求职信息填充工具 - 主控脚本
作者: chen luoli
版本: 1.0
功能: 自动填充招聘网站的个人信息，支持智能问答式配置管理
"""

import sys
import traceback
import config_manager
import zhipin_filler


def show_banner():
    """显示程序横幅"""
    print("=" * 60)
    print("      🚀 自动求职信息填充工具 v1.0")
    print("=" * 60)
    print("功能特点:")
    print("• 智能配置管理 - 按需询问，永久记忆")
    print("• 自动信息填充 - 节省时间，提高效率")
    print("• 多网站支持 - 可扩展到不同招聘平台")
    print("• 安全可靠 - 本地存储，保护隐私")
    print("=" * 60)


def show_menu():
    """显示主菜单"""
    print("\n📋 请选择操作:")
    print("1. 启动 BOSS直聘 信息填充")
    print("2. 查看当前配置信息")
    print("3. 手动编辑配置信息")
    print("4. 清空所有配置")
    print("5. 帮助信息")
    print("0. 退出程序")
    print("-" * 30)


def handle_zhipin_filling():
    """处理BOSS直聘填充"""
    print("\n🎯 准备启动BOSS直聘信息填充...")
    print("\n⚠️  重要提醒:")
    print("1. 请确保已安装Chrome浏览器")
    print("2. 请确保网络连接正常")
    print("3. 准备好您的登录账号信息")
    print("4. 建议关闭其他不必要的程序以获得最佳性能")

    confirm = input("\n是否继续? (y/n): ").strip().lower()
    if confirm in ['y', 'yes', '是']:
        try:
            filler = zhipin_filler.ZhipinFiller()
            success = filler.start_filling_process()

            if success:
                print("\n✅ 填充流程完成!")
            else:
                print("\n❌ 填充流程出现问题，请检查错误信息")

        except KeyboardInterrupt:
            print("\n\n⏹️  用户中断操作")
        except Exception as e:
            print(f"\n❌ 程序异常: {e}")
            print("\n详细错误信息:")
            traceback.print_exc()
    else:
        print("操作已取消")


def handle_view_config():
    """处理查看配置"""
    print("\n📄 当前配置信息:")
    config_manager.show_config()


def handle_edit_config():
    """处理手动编辑配置"""
    print("\n✏️  手动编辑配置信息")
    print("请按照 [节名.键名] 的格式输入要编辑的配置项")
    print("例如: PersonalInfo.name 或 WorkInfo.expected_salary")
    print("输入 'list' 查看所有可用配置项")
    print("输入 'quit' 返回主菜单")

    while True:
        user_input = input("\n请输入配置项名称: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        elif user_input.lower() == 'list':
            config_manager.show_config()
            continue
        elif '.' not in user_input:
            print("❌ 格式错误，请使用 [节名.键名] 格式")
            continue

        try:
            section, key = user_input.split('.', 1)
            current_value = config_manager.get_config(section, key, "未设置")
            print(f"当前值: {current_value}")

            new_value = input("请输入新值 (直接回车保持不变): ").strip()
            if new_value:
                config_manager.set_config(section, key, new_value)
                print("✅ 配置已更新")
            else:
                print("配置未更改")

        except Exception as e:
            print(f"❌ 编辑配置失败: {e}")


def handle_clear_config():
    """处理清空配置"""
    print("\n⚠️  危险操作: 清空所有配置")
    print("这将删除所有已保存的个人信息!")

    confirm1 = input("确定要继续吗? (yes/no): ").strip().lower()
    if confirm1 == 'yes':
        confirm2 = input("请再次确认，输入 'DELETE' 来执行清空操作: ").strip()
        if confirm2 == 'DELETE':
            try:
                import os
                if os.path.exists("config.ini"):
                    os.remove("config.ini")
                    print("✅ 配置文件已删除，程序重启后将重新创建")
                else:
                    print("ℹ️  配置文件不存在")
            except Exception as e:
                print(f"❌ 删除配置文件失败: {e}")
        else:
            print("操作已取消")
    else:
        print("操作已取消")


def show_help():
    """显示帮助信息"""
    print("\n📚 帮助信息")
    print("-" * 40)
    print("🔧 系统要求:")
    print("• Python 3.9+")
    print("• Chrome 浏览器")
    print("• selenium 库")
    print("")
    print("🚀 使用流程:")
    print("1. 首次运行会创建默认配置文件")
    print("2. 选择要填充的招聘网站")
    print("3. 程序会打开浏览器，请手动登录")
    print("4. 程序会自动填充已有信息")
    print("5. 对于缺失信息，程序会询问您")
    print("6. 您输入的信息会自动保存，下次无需重复输入")
    print("")
    print("⚡ 效率提升:")
    print("• 一次配置，多次使用")
    print("• 支持多个招聘网站")
    print("• 自动记忆新增信息")
    print("")
    print("🔒 隐私保护:")
    print("• 所有信息存储在本地 config.ini 文件")
    print("• 不会上传任何个人信息")
    print("• 可随时删除配置文件")
    print("")
    print("❓ 常见问题:")
    print("• 如果浏览器无法启动，请检查Chrome是否已安装")
    print("• 如果找不到元素，可能网站页面有更新，请联系开发者")
    print("• 建议在网络稳定的环境下使用")


def main():
    """主函数"""
    try:
        show_banner()

        while True:
            show_menu()
            choice = input("请输入选项数字: ").strip()

            if choice == '1':
                handle_zhipin_filling()
            elif choice == '2':
                handle_view_config()
            elif choice == '3':
                handle_edit_config()
            elif choice == '4':
                handle_clear_config()
            elif choice == '5':
                show_help()
            elif choice == '0':
                print("\n👋 感谢使用，祝您求职顺利!")
                break
            else:
                print("❌ 无效选项，请重新选择")

            # 等待用户按键继续
            if choice != '0':
                input("\n按回车键继续...")

    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见!")
    except Exception as e:
        print(f"\n❌ 程序发生未预期的错误: {e}")
        print("\n详细错误信息:")
        traceback.print_exc()
        print("\n请将错误信息反馈给开发者")


if __name__ == "__main__":
    main()