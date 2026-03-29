#!/bin/bash
# NBA Stats API - 启动脚本

echo "🏀 启动 NBA Stats API 服务..."

# 进入项目目录
cd "$(dirname "$0")"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "⚠️ 虚拟环境不存在，创建中..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# 启动服务
echo "🚀 启动 FastAPI 服务 (http://localhost:3000)"
echo "📖 API 文档：http://localhost:3000/docs"

python src/main.py
