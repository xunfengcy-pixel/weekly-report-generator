@echo off
chcp 65001 >nul
echo 🚀 周报生成器安装脚本
echo ======================

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python
    echo.
    echo 安装方式：
    echo   1. 访问 https://www.python.org/downloads/ 下载安装
    echo   2. 安装时勾选 "Add Python to PATH"
    pause
    exit /b 1
)

for /f "tokens=*" %%a in ('python --version') do set PYTHON_VERSION=%%a
echo ✅ Python 已安装: %PYTHON_VERSION%

:: 进入脚本所在目录
cd /d "%~dp0"

:: 创建虚拟环境
echo 📦 创建虚拟环境...
python -m venv venv

:: 激活虚拟环境
echo 🔌 激活虚拟环境...
call venv\Scripts\activate.bat

:: 安装依赖
echo 📥 安装依赖...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ 安装完成！
echo.
echo 📂 项目路径: %~dp0
echo.
echo 启动命令：
echo   cd %~dp0
echo   venv\Scripts\activate.bat
echo   streamlit run app.py
echo.
set /p answer="是否现在启动？(y/n): "
if /i "%answer%"=="y" (
    streamlit run app.py
)

pause
