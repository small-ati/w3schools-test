# W3Schools 回归测试工具

## 项目简介
这是一个用 Python 编写的自动化回归测试工具，用于验证 W3Schools Python 教程页面的核心功能是否正常。

## 功能列表
- 接口测试：检查首页状态码和标题
- 界面测试：检查导航栏链接完整性
- 随机点击验证：随机点击导航栏链接，验证跳转后页面标题
- 失败自动截图：测试失败时自动保存浏览器截图

## 技术栈
- Python 3
- pytest（测试框架）
- requests（接口测试）
- Selenium（界面自动化）
- Git（版本控制）

## 项目结构
- `conftest.py`：pytest 公共配置，包含网站配置和命令行参数
- `test_w3schools.py`：测试用例文件
- `.gitignore`：Git 忽略文件配置
- `README.md`：项目说明

## 使用方法
1. 安装依赖：pip install pytest requests selenium
2. 下载与你的 Edge 浏览器版本匹配的 msedgedriver.exe，放在项目目录下
3. 在项目所在文件夹里打开终端运行：pytest test_w3schools.py -v（项目所在文件夹需要msedgedriver.exe ）

## 作者
陈天泰（初中学历，自学 Python 自动化测试转行中）