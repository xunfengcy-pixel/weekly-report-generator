@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 推送到 GitHub 并触发自动打包
echo ========================================
echo.

:: 检查 git
where git >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 git，请先安装 Git
    echo 下载地址: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git 已安装

:: 获取当前目录名作为项目名
for %%I in (.) do set PROJECT_NAME=%%~nxI
echo 📁 项目名称: %PROJECT_NAME%
echo.

:: 检查是否已初始化 git
if not exist .git (
    echo 📦 初始化 Git 仓库...
    git init
    git add .
    git commit -m "Initial commit"
) else (
    echo ✅ Git 仓库已存在
)

:: 检查是否已连接远程仓库
git remote -v >nul 2>&1
if errorlevel 1 (
    echo.
    echo 🔗 请先在 GitHub 创建仓库，然后输入仓库地址
    echo 格式: https://github.com/你的用户名/%PROJECT_NAME%.git
    set /p REMOTE_URL="仓库地址: "
    
    git remote add origin %REMOTE_URL%
    git branch -M main
    git push -u origin main
) else (
    echo ✅ 远程仓库已配置
    echo.
    echo 📤 推送代码...
    git add .
    git commit -m "Update code"
    git push origin main
)

echo.
echo ========================================
echo 🏷️  创建版本标签触发打包
echo ========================================
echo.

:: 获取当前版本号
for /f "tokens=*" %%a in ('git tag --sort=-creatordate 2^>nul ^| head -1') do set LAST_TAG=%%a

if "%LAST_TAG%"=="" (
    set NEW_TAG=v1.0.0
) else (
    :: 简单版本号递增
    set NEW_TAG=v1.0.1
)

echo 最新标签: %LAST_TAG%
echo 建议新标签: %NEW_TAG%
echo.
set /p TAG="输入版本标签 (直接回车使用 %NEW_TAG%): "
if "%TAG%"=="" set TAG=%NEW_TAG%

echo.
echo 🏷️  创建标签: %TAG%
git tag -a %TAG% -m "版本 %TAG%"

echo 📤 推送标签...
git push origin %TAG%

echo.
echo ========================================
echo ✅ 完成！
echo ========================================
echo.
echo 打包进度请访问:
echo   https://github.com/你的用户名/%PROJECT_NAME%/actions
echo.
echo 打包完成后下载地址:
echo   https://github.com/你的用户名/%PROJECT_NAME%/releases
echo.
pause
