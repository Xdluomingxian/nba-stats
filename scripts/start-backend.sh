#!/bin/bash

# 启动后端服务
# 使用: bash scripts/start-backend.sh

set -e

# 颜色定义
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  启动 LeBron Stats 后端服务${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

BACKEND_PORT=3000

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_PATH="$PROJECT_ROOT/backend"

# 检查后端目录
if [ ! -d "$BACKEND_PATH" ]; then
    echo -e "${RED}❌ 后端目录不存在: $BACKEND_PATH${NC}"
    exit 1
fi

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo -e "${RED}❌ 未找到 Python，请安装 Python 3.8+${NC}"
    echo -e "${GRAY}   下载地址: https://www.python.org/downloads/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python: $PYTHON_CMD${NC}"

# 检查虚拟环境
VENV_PATH="$BACKEND_PATH/venv"
VENV_PYTHON="$VENV_PATH/bin/python"

if [ -f "$VENV_PYTHON" ]; then
    echo -e "${GREEN}✅ 使用虚拟环境: $VENV_PATH${NC}"
    PYTHON_EXE="$VENV_PYTHON"
else
    echo -e "${YELLOW}⚠️  使用系统 Python${NC}"
    echo -e "${GRAY}   建议创建虚拟环境: python -m venv venv${NC}"
    PYTHON_EXE="$PYTHON_CMD"
fi

# 检查依赖
echo ""
echo -e "${YELLOW}📦 检查依赖...${NC}"

# 尝试导入 fastapi
if ! $PYTHON_EXE -c "import fastapi; import nba_api" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  依赖未安装，正在安装...${NC}"
    cd "$BACKEND_PATH"
    $PYTHON_EXE -m pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 依赖安装失败${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
else
    echo -e "${GREEN}✅ 依赖已安装${NC}"
fi

echo ""
echo -e "${GREEN}🚀 启动后端服务...${NC}"
echo -e "${GRAY}   端口: $BACKEND_PORT${NC}"
echo -e "${GRAY}   地址: http://localhost:$BACKEND_PORT${NC}"
echo ""

# 启动后端
cd "$BACKEND_PATH"
$PYTHON_EXE main.py
