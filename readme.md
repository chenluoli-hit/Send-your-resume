# 🚀 自动求职信息填充工具

一个智能的求职信息自动填充工具，帮助求职者快速填写招聘网站上的标准化个人信息，节省时间，提高求职效率。

## ✨ 核心特性

### 🧠 智能配置管理
- **按需询问**: 只在需要时询问缺失信息
- **永久记忆**: 一次输入，终身使用
- **智能补充**: 自动保存新增信息到配置文件

### ⚡ 自动化填充
- **多字段支持**: 姓名、联系方式、教育背景、工作经验等
- **智能识别**: 自动识别网站表单字段
- **容错处理**: 优雅处理异常和错误情况

### 🔒 隐私保护
- **本地存储**: 所有信息存储在本地配置文件
- **无需联网**: 配置信息不会上传到服务器
- **用户控制**: 可随时查看、编辑或删除配置

## 📋 系统要求

- **Python**: 3.9+
- **浏览器**: Chrome 浏览器
- **操作系统**: Windows/macOS/Linux

## 🛠️ 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd job-application-filler
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 安装 ChromeDriver
- 方法一: 使用 webdriver-manager (推荐)
  ```bash
  pip install webdriver-manager
  ```
- 方法二: 手动下载并配置 ChromeDriver
  - 访问 [ChromeDriver下载页面](https://chromedriver.chromium.org/)
  - 下载对应Chrome版本的驱动
  - 将驱动添加到系统PATH

### 4. 运行程序
```bash
python main.py
```

## 🎯 使用指南

### 首次使用流程

1. **启动程序**
   ```bash
   python main.py
   ```

2. **选择填充功能**
   - 从主菜单选择 "1. 启动 BOSS直聘 信息填充"

3. **手动登录**
   - 程序会打开浏览器并导航到招聘网站
   - 请手动完成登录过程
   - 导航到简历编辑页面

4. **自动填充开始**
   - 程序会自动填充已有信息
   - 对于缺失信息，会在命令行询问您
   - 输入的信息会自动保存，下次无需重复输入

### 配置管理

#### 查看当前配置
```bash
# 在主菜单选择选项 2
```

#### 手动编辑配置
```bash
# 在主菜单选择选项 3
# 使用格式: PersonalInfo.name
```

#### 清空所有配置
```bash
# 在主菜单选择选项 4
# 需要二次确认
```

## 📁 项目结构

```
job-application-filler/
├── main.py              # 主控脚本，程序入口
├── config_manager.py    # 配置管理核心模块
├── browser_engine.py    # 浏览器操作引擎
├── zhipin_filler.py     # BOSS直聘填充脚本
├── config.ini           # 配置文件（自动生成）
├── requirements.txt     # 依赖包列表
└── README.md           # 项目说明文档
```

## 🔧 核心模块说明

### config_manager.py
**功能**: 项目的记忆核心
- `get_or_ask()`: 核心函数，实现"按需询问"功能
- `get_config()`: 直接获取配置值
- `set_config()`: 设置配置值
- `show_config()`: 显示所有配置

### browser_engine.py
**功能**: 浏览器操作引擎
- 封装 Selenium 基础操作
- 提供统一的浏览器自动化接口
- 支持元素查找、填充、点击等操作

### zhipin_filler.py
**功能**: BOSS直聘专用填充脚本
- 针对 BOSS直聘 网站的表单结构
- 调用配置管理器获取信息
- 实现具体的填充逻辑

## 📊 验收标准 (Definition of Done)

- ✅ 脚本可以成功打开目标网站的简历编辑页面
- ✅ 对于配置文件中已存在的信息，能够自动读取并填写
- ✅ 对于配置文件中不存在的信息，能够暂停并询问用户
- ✅ 用户输入的信息能够被自动保存到配置文件
- ✅ 下次运行时，上次补充的信息能够被自动填充

## 🚧 扩展支持

### 添加新网站支持

1. **创建新的填充脚本**
   ```python
   # 例如: lagou_filler.py
   import config_manager
   import browser_engine
   
   class LagouFiller:
       def fill_profile(self):
           # 实现具体填充逻辑
           pass
   ```

2. **在主脚本中添加菜单选项**
   ```python
   # 在 main.py 中添加新的处理函数
   ```

### 自定义字段配置

可以通过修改配置文件添加自定义字段：

```ini
[CustomInfo]
linkedin_url = 
portfolio_url = 
expected_location = 
```

## ⚠️ 注意事项

1. **合规使用**
   - 仅用于填充自己的真实信息
   - 遵守各招聘网站的使用条款
   - 不要用于恶意或违法目的

2. **网站更新**
   - 招聘网站可能会更新页面结构
   - 如遇到元素无法识别，请及时反馈

3. **隐私保护**
   - 配置文件包含个人信息，请妥善保管
   - 不要在公共场所或他人设备上使用
   - 定期清理不需要的配置信息

## 🐛 故障排除

### 常见问题

**问题1**: 浏览器无法启动
```
解决方案:
1. 确认已安装 Chrome 浏览器
2. 确认 ChromeDriver 版本与 Chrome 版本匹配
3. 尝试重新安装 webdriver-manager
```

**问题2**: 找不到页面元素
```
解决方案:
1. 确认已正确导航到填充页面
2. 检查网站是否有更新
3. 尝试刷新页面后重新运行
```

**问题3**: 配置文件损坏
```
解决方案:
1. 删除 config.ini 文件
2. 重新运行程序自动生成新配置
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (当前版本)
- ✨ 初始版本发布
- 🎯 支持 BOSS直聘 信息填充
- 🧠 智能配置管理系统
- ⚡ 自动化浏览器操作
- 🔒 本地隐私保护

### 未来计划
- 🔜 支持更多招聘网站 
- 🔜 支持简历模板导入
- 🔜 支持批量申请职位
- 🔜 添加 GUI 界面

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 💬 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: 1292593513@qq.com
- 🐛 Issues: [GitHub Issues](https://github.com/chenluoli-hit/Send-your-resume)

---

⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！
