#!/bin/bash

echo "🚀 周报生成器安装脚本"
echo "======================"

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python3"
    echo ""
    echo "安装方式："
    echo "  1. 访问 https://www.python.org/downloads/ 下载安装"
    echo "  2. 或使用 Homebrew: brew install python3"
    exit 1
fi

echo "✅ Python3 已安装: $(python3 --version)"

# 进入脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ 安装完成！"
echo ""
echo "📂 项目路径: $SCRIPT_DIR"
echo ""
echo "启动命令："
echo "  cd $SCRIPT_DIR"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
read -p "是否现在启动？(y/n): " answer
if [[ $answer == "y" || $answer == "Y" ]]; then
    streamlit run app.py
fi
