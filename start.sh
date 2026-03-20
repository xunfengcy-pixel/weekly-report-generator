#!/bin/bash
# 周报生成器 Docker 启动脚本（Mac/Linux）

echo "🚀 启动周报生成器..."
echo "=================="

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 未找到 Docker"
    echo ""
    echo "请先安装 Docker Desktop："
    echo "  https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 未找到 Docker Compose"
    echo "请确保 Docker Desktop 已正确安装"
    exit 1
fi

echo "✅ Docker 已安装"

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    echo "❌ Docker 服务未运行"
    echo "请启动 Docker Desktop"
    exit 1
fi

echo "✅ Docker 服务运行中"

# 进入脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 创建数据目录
mkdir -p data

# 检查是否存在已运行的容器
if docker ps | grep -q "weekly-report"; then
    echo ""
    echo "⚠️  周报生成器已在运行"
    echo "🌐 访问地址: http://localhost:8501"
    echo ""
    read -p "是否重新启动？(y/n): " restart
    if [[ $restart == "y" || $restart == "Y" ]]; then
        docker-compose down
    else
        echo ""
        echo "📋 常用命令："
        echo "  查看日志: docker-compose logs -f"
        echo "  停止服务: docker-compose down"
        exit 0
    fi
fi

# 构建并启动
echo ""
echo "📦 构建镜像..."
docker-compose build

echo ""
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if docker ps | grep -q "weekly-report"; then
    echo ""
    echo "✅ 周报生成器启动成功！"
    echo ""
    echo "🌐 访问地址: http://localhost:8501"
    echo ""
    echo "📋 常用命令："
    echo "  查看日志: docker-compose logs -f"
    echo "  停止服务: docker-compose down"
    echo "  重启服务: docker-compose restart"
    echo ""
    
    # 尝试自动打开浏览器
    if command -v open &> /dev/null; then
        open http://localhost:8501
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8501
    fi
else
    echo ""
    echo "❌ 启动失败，查看日志："
    docker-compose logs
fi
