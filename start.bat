@echo off
chcp 65001 >nul
echo 🚀 启动周报生成器...
echo ==================

:: 检查 Docker 是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Docker
    echo.
    echo 请先安装 Docker Desktop：
    echo   https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo ✅ Docker 已安装

:: 检查 Docker 是否运行
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker 服务未运行
    echo 请启动 Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker 服务运行中

:: 进入脚本所在目录
cd /d "%~dp0"

:: 创建数据目录
if not exist data mkdir data

:: 检查是否存在已运行的容器
docker ps | findstr "weekly-report" >nul
if %errorlevel% == 0 (
    echo.
    echo ⚠️  周报生成器已在运行
    echo 🌐 访问地址: http://localhost:8501
    echo.
    set /p restart="是否重新启动？(y/n): "
    if /i "%restart%"=="y" (
        docker-compose down
    ) else (
        echo.
        echo 📋 常用命令：
        echo   查看日志: docker-compose logs -f
        echo   停止服务: docker-compose down
        pause
        exit /b 0
    )
)

echo.
echo 📦 构建镜像...
docker-compose build

echo.
echo 🚀 启动服务...
docker-compose up -d

:: 等待服务启动
echo.
echo ⏳ 等待服务启动...
timeout /t 5 /nobreak >nul

:: 检查服务状态
docker ps | findstr "weekly-report" >nul
if %errorlevel% == 0 (
    echo.
    echo ✅ 周报生成器启动成功！
    echo.
    echo 🌐 访问地址: http://localhost:8501
    echo.
    echo 📋 常用命令：
    echo   查看日志: docker-compose logs -f
    echo   停止服务: docker-compose down
    echo   重启服务: docker-compose restart
    echo.
    
    :: 尝试自动打开浏览器
    start http://localhost:8501
) else (
    echo.
    echo ❌ 启动失败，查看日志：
    docker-compose logs
)

pause
