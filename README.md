# 综合诉讼维权中心周报生成器

基于 Streamlit 的周报生成工具，支持跨平台运行（Windows / macOS / Linux）。

## 功能特性

- 📊 六大板块数据管理（劳动人事、竞业限制、商业秘密、公司事务、商标版权专利、不正当竞争、其他案件）
- 📝 重点案件摘要编辑
- 🔗 文档链接管理
- 📁 案件详情编辑（支持多负责人、状态标签）
- 💾 自动保存与数据恢复
- 👁️ HTML 预览、下载、复制源代码
- 🎨 现代化 UI 设计

## 跨平台部署指南

### macOS 部署步骤

#### 1. 复制项目文件

将 `weekly_report_generator` 文件夹复制到 MacBook 的任意位置，例如 `~/Documents/`

#### 2. 打开终端

按 `Cmd + Space` 搜索 "Terminal" 打开终端

#### 3. 进入项目目录

```bash
cd ~/Documents/weekly_report_generator
```

#### 4. 创建虚拟环境（推荐）

```bash
python3 -m venv venv
```

#### 5. 激活虚拟环境

```bash
source venv/bin/activate
```

#### 6. 安装依赖

```bash
pip install streamlit
```

#### 7. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

---

### Windows 部署步骤

#### 1. 进入项目目录

```cmd
cd C:\Users\YourName\Documents\weekly_report_generator
```

#### 2. 创建虚拟环境

```cmd
python -m venv venv
```

#### 3. 激活虚拟环境

```cmd
venv\Scripts\activate
```

#### 4. 安装依赖

```cmd
pip install streamlit
```

#### 5. 运行应用

```cmd
streamlit run app.py
```

---

### Linux 部署步骤

与 macOS 步骤相同：

```bash
cd ~/weekly_report_generator
python3 -m venv venv
source venv/bin/activate
pip install streamlit
streamlit run app.py
```

---

## 一键安装脚本

### macOS / Linux 一键脚本

创建文件 `setup.sh`：

```bash
#!/bin/bash

echo "🚀 周报生成器安装脚本"
echo "======================"

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python3"
    exit 1
fi

echo "✅ Python3 已安装"

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install --upgrade pip
pip install streamlit

echo ""
echo "✅ 安装完成！"
echo ""
echo "启动命令："
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
read -p "是否现在启动？(y/n): " answer
if [[ $answer == "y" || $answer == "Y" ]]; then
    streamlit run app.py
fi
```

使用方法：
```bash
chmod +x setup.sh
./setup.sh
```

---

### Windows 一键脚本

创建文件 `setup.bat`：

```batch
@echo off
chcp 65001 >nul
echo 🚀 周报生成器安装脚本
echo ======================

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

echo ✅ Python 已安装

:: 创建虚拟环境
echo 📦 创建虚拟环境...
python -m venv venv

:: 激活虚拟环境
echo 🔌 激活虚拟环境...
call venv\Scripts\activate.bat

:: 安装依赖
echo 📥 安装依赖...
pip install --upgrade pip
pip install streamlit

echo.
echo ✅ 安装完成！
echo.
echo 启动命令：
echo   venv\Scripts\activate.bat
echo   streamlit run app.py
echo.
set /p answer="是否现在启动？(y/n): "
if /i "%answer%"=="y" (
    streamlit run app.py
)

pause
```

双击运行 `setup.bat` 即可

---

## 项目结构

```
weekly_report_generator/
├── app.py              # 主应用入口
├── config.py           # 配置文件（板块、负责人、默认值等）
├── template.html       # HTML 周报模板
├── requirements.txt    # Python 依赖列表
├── README.md           # 本说明文档
├── setup.sh            # macOS/Linux 一键安装脚本
├── setup.bat           # Windows 一键安装脚本
└── weekly_report_autosave.json  # 自动保存数据（运行时生成）
```

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `streamlit run app.py` | 启动应用 |
| `source venv/bin/activate` | macOS/Linux 激活虚拟环境 |
| `venv\Scripts\activate.bat` | Windows 激活虚拟环境 |
| `deactivate` | 退出虚拟环境 |

---

## 数据迁移

自动保存的数据文件 `weekly_report_autosave.json` 可以直接复制到另一台电脑使用，实现数据无缝迁移。

---

## 注意事项

1. **首次运行**：会自动在浏览器打开应用，如未打开请手动访问 `http://localhost:8501`
2. **端口占用**：如果 8501 端口被占用，Streamlit 会自动使用其他端口
3. **数据安全**：自动保存的数据存储在本地，不会上传到云端

---

## 技术支持

如有问题，请检查：
1. Python 版本是否 >= 3.8
2. 虚拟环境是否正确激活
3. 依赖是否完整安装
