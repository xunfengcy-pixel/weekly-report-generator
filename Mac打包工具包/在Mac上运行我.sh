#!/bin/bash
# 周报生成器 Mac 打包脚本
# 使用方法：
#   方法1: 双击运行（如果不行，用方法2）
#   方法2: 打开终端，执行: bash 在Mac上运行我.sh

echo "🚀 周报生成器 Mac 打包工具"
echo "=========================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3"
    echo ""
    echo "请先安装 Python3："
    echo "  方法1: 访问 https://www.python.org/downloads/ 下载安装"
    echo "  方法2: 在终端执行: brew install python3"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

echo "✅ Python3 已安装: $(python3 --version)"
echo ""

# 安装打包工具
echo "📦 安装打包工具..."
pip3 install --user pyinstaller streamlit

# 检查安装是否成功
if ! command -v pyinstaller &> /dev/null; then
    # 尝试从用户目录找
    export PATH="$PATH:$HOME/Library/Python/3.11/bin:$HOME/Library/Python/3.9/bin:$HOME/Library/Python/3.10/bin"
fi

echo ""
echo "🔨 开始打包..."
echo ""

# 执行打包
python3 -m PyInstaller \
    --onefile \
    --name "周报生成器" \
    --add-data "app.py:." \
    --add-data "config.py:." \
    --add-data "template.html:." \
    --clean \
    run_app.py

# 检查打包结果
if [ ! -f "dist/周报生成器" ]; then
    echo ""
    echo "❌ 打包失败，请检查上面的错误信息"
    read -p "按回车键退出..."
    exit 1
fi

echo ""
echo "✅ 可执行文件已生成！"
echo ""

# 创建应用包
echo "📁 创建 Mac 应用包..."
mkdir -p "dist/周报生成器.app/Contents/MacOS"
mkdir -p "dist/周报生成器.app/Contents/Resources"

# 复制可执行文件
cp "dist/周报生成器" "dist/周报生成器.app/Contents/MacOS/"

# 创建 Info.plist
cat > "dist/周报生成器.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>zh_CN</string>
    <key>CFBundleExecutable</key>
    <string>周报生成器</string>
    <key>CFBundleIdentifier</key>
    <string>com.weeklyreport.generator</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>周报生成器</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo ""
echo "🎉 打包完成！"
echo ""
echo "📂 输出文件："
echo "  📁 dist/周报生成器.app （Mac 应用程序）"
echo "  ⚙️  dist/周报生成器 （命令行版本）"
echo ""
echo "📦 分发方式："
echo "  1. 压缩 dist/周报生成器.app 发给用户"
echo "  2. 用户解压后双击即可运行"
echo ""
echo "⚠️  注意："
echo "  首次运行可能需要右键打开（Control+点击）"
echo "  或在终端执行: xattr -cr 周报生成器.app"
echo ""

# 询问是否打开输出目录
read -p "是否打开输出目录？(y/n): " open_dir
if [[ $open_dir == "y" || $open_dir == "Y" ]]; then
    open "$SCRIPT_DIR/dist"
fi

echo ""
read -p "按回车键退出..."
