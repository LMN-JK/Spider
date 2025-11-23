# 项目介绍
这是一个基于Scrapy的爬虫项目，用于从指定的网站上提取数据。

git clone https://github.com/yourusername/Spider.git
cd Spider

# miniconda环境
# 使用miniconda来管理项目依赖（提前下载miniconda并添加到环境变量，版本为miniconda3-2023.11.0-1）
# 创建miniconda环境（Windows）
conda create -n spider python=3.12
# 激活miniconda环境（Windows）
conda activate spider
# 安装依赖
pip install -r requirements.txt

1. 项目初始化阶段
在项目根目录执行（通常是包含scrapy.cfg的文件夹）
# 进入Scrapy项目目录
cd D:\PycharmProjects\MyProject\Spider

# 初始化Git仓库
git init

# 检查状态
git status
2. 创建合适的.gitignore文件
在项目根目录创建.gitignore文件，内容如下：
# Python相关
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cgs
*.egg
MANIFEST

# Scrapy特定
.scrapy

# 环境相关
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db

# 日志文件
*.log
logs/

# 数据文件（爬虫数据通常不上传）
*.json
*.csv
*.xml
data/

# 临时文件
temp/
tmp/

# 增加自己的文件


3. 配置Git用户信息
# 设置全局用户信息（用于所有项目）
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"

# 或者为当前项目单独设置（推荐）
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub邮箱"
4. 添加文件到Git仓库
# 添加所有文件到暂存区
git add .

# 或者选择性添加
git add scrapy.cfg
git add proj/
git add .gitignore

# 查看暂存状态
git status
5. 提交代码
# 提交到本地仓库
git commit -m "初始提交：添加Scrapy项目文件"

# 查看提交历史
git log --oneline
6. 在GitHub上创建远程仓库
在GitHub网站操作：
登录GitHub
点击右上角"+" → "New repository"
填写仓库信息：
Repository name: Spider（与本地文件夹名一致）
Description: Scrapy爬虫项目
选择Public或Private
不要勾选"Add a README file"（因为本地已有代码）
不要勾选"Add .gitignore"（因为我们已经创建了）
点击"Create repository"
7. 连接本地仓库与GitHub远程仓库
# 添加远程仓库（使用你的GitHub用户名）
git remote add origin https://github.com/LMN-JK/Spider.git

# 验证远程仓库配置
git remote -v
8. 配置代理（针对GitHub）
# 为GitHub设置代理（使用你的代理端口）
git config --global http.https://github.com.proxy socks5://127.0.0.1:7897

# 当前设置的代理：
# 只对github.com使用代理
git config --global http.https://github.com.proxy socks5://127.0.0.1:7897

# 常用的clash代理配置:
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 取消所有代理设置
git config --global --unset http.proxy
git config --global --unset https.proxy

# 或只取消GitHub的代理
git config --global --unset http.https://github.com.proxy

9. 推送代码到GitHub
# 首次推送，设置上游分支
git push -u origin main

# 如果默认分支是master，则使用：
git push -u origin master

# 后续推送只需
git push
10. 在VS Code中的操作流程
第一次设置后，日常开发流程：
修改代码​ → 在VS Code中编辑文件
暂存更改​ → 在源代码管理面板点击"+"或输入git add .
提交更改​ → 输入提交信息，点击提交
推送到远程​ → 点击同步更改或推送按钮
11. 项目文件结构示例
你的项目应该有这样的结构：
Spider/
├── .git/                    # Git仓库（隐藏文件夹）
├── .gitignore              # Git忽略规则
├── scrapy.cfg              # Scrapy配置文件
└── proj/                   # 项目代码
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        ├── __init__.py
        └── example.py
12. 验证设置是否成功
# 检查所有配置
git config --list

# 查看远程仓库
git remote -v

# 查看分支情况
git branch -a

# 测试从远程拉取（确保连接正常）
git pull origin main
重要提示
首次推送前确保GitHub仓库是空的（没有README等文件）
代理设置只在需要访问GitHub时使用
提交信息要清晰描述更改内容
定期推送避免代码丢失


