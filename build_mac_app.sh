#!/bin/bash
# Mac 应用打包脚本
# 在 MacBook 上运行此脚本生成独立应用

echo "🚀 开始打包周报生成器 Mac 应用..."
echo "================================"

# 检查是否在 macOS 上运行
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本需要在 macOS 上运行"
    echo "请在 MacBook 上执行此脚本"
    exit 1
fi

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3"
    exit 1
fi

echo "✅ Python3 已安装"

# 安装 pyinstaller
echo "📦 安装打包工具..."
pip3 install pyinstaller streamlit

# 创建打包入口脚本
cat > run_app.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import subprocess
import webbrowser
import time
import signal

def get_resource_path(relative_path):
    """获取资源文件路径（支持打包后的路径）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    # 设置工作目录
    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    
    print("🚀 启动周报生成器...")
    print("=" * 40)
    
    # 启动 Streamlit
    env = os.environ.copy()
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    process = subprocess.Popen(
        [sys.executable, '-m', 'streamlit', 'run', 'app.py', 
         '--server.port=8501', 
         '--server.address=localhost',
         '--browser.gatherUsageStats=false'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待服务启动
    time.sleep(3)
    
    # 打开浏览器
    url = 'http://localhost:8501'
    print(f"✅ 服务已启动，正在打开浏览器...")
    print(f"🌐 访问地址: {url}")
    webbrowser.open(url)
    
    print("\n⚠️  请不要关闭此窗口，关闭窗口将停止服务")
    print("=" * 40)
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 正在关闭服务...")
        process.terminate()
        process.wait()
        print("✅ 服务已停止")

if __name__ == '__main__':
    main()
EOF

# 创建打包配置
cat > weekly_report.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

block_cipher = None

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('config.py', '.'),
        ('template.html', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'pandas',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='周报生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.icns' if os.path.exists('icon.icns') else None,
)
EOF

# 执行打包
echo "🔨 开始打包..."
pyinstaller --clean weekly_report.spec

# 创建应用包结构
echo "📁 创建应用包..."
APP_NAME="周报生成器.app"
mkdir -p "dist/$APP_NAME/Contents/MacOS"
mkdir -p "dist/$APP_NAME/Contents/Resources"

# 移动可执行文件
mv "dist/周报生成器" "dist/$APP_NAME/Contents/MacOS/"

# 创建 Info.plist
cat > "dist/$APP_NAME/Contents/Info.plist" << 'EOF'
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

# 创建启动脚本（双击直接运行）
cat > "dist/启动周报生成器.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./周报生成器.app/Contents/MacOS/周报生成器
EOF
chmod +x "dist/启动周报生成器.command"

echo ""
echo "✅ 打包完成！"
echo ""
echo "📦 输出文件："
echo "  - dist/周报生成器.app （应用程序包）"
echo "  - dist/启动周报生成器.command （双击启动脚本）"
echo ""
echo "💡 使用方式："
echo "  1. 将整个 dist 文件夹复制给用户"
echo "  2. 用户双击 '启动周报生成器.command' 即可运行"
echo ""
