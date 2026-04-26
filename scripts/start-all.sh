#!/bin/bash

# 一键启动脚本 - 启动前后端服务
# 使用: bash scripts/start-all.sh

set -e

# 颜色定义
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  LeBron Stats - 全栈项目启动器${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

BACKEND_PORT=3000
FRONTEND_PORT=5173

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 检查后端端口
if check_port $BACKEND_PORT; then
    echo -e "${YELLOW}⚠️  端口 $BACKEND_PORT 已被占用，后端可能已在运行${NC}"
else
    echo -e "${GREEN}✅ 端口 $BACKEND_PORT 可用${NC}"
fi

# 检查前端端口
if check_port $FRONTEND_PORT; then
    echo -e "${YELLOW}⚠️  端口 $FRONTEND_PORT 已被占用，前端可能已在运行${NC}"
else
    echo -e "${GREEN}✅ 端口 $FRONTEND_PORT 可用${NC}"
fi

echo ""

# 解析参数
BACKEND_ONLY=false
FRONTEND_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            BACKEND_ONLY=true
            shift
            ;;
        --frontend-only)
            FRONTEND_ONLY=true
            shift
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            echo "用法: $0 [--backend-only|--frontend-only]"
            exit 1
            ;;
    esac
done

# 启动后端
if [ "$FRONTEND_ONLY" = false ]; then
    echo -e "${GREEN}🚀 正在启动后端服务...${NC}"
    
    BACKEND_PATH="$PROJECT_ROOT/backend"
    
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
        exit 1
    fi
    
    echo -e "${GRAY}   Python: $PYTHON_CMD${NC}"
    
    # 检查虚拟环境
    VENV_PATH="$BACKEND_PATH/venv"
    VENV_PYTHON="$VENV_PATH/bin/python"
    
    if [ -f "$VENV_PYTHON" ]; then
        echo -e "${GRAY}   使用虚拟环境${NC}"
        PYTHON_EXE="$VENV_PYTHON"
    else
        echo -e "${YELLOW}   使用系统 Python（建议创建虚拟环境）${NC}"
        PYTHON_EXE="$PYTHON_CMD"
    fi
    
    # 启动后端（后台运行）
    cd "$BACKEND_PATH"
    $PYTHON_EXE main.py &
    BACKEND_PID=$!
    
    echo -e "${GRAY}   后端服务启动中...${NC}"
    sleep 3
    
    # 检查后端是否启动成功
    RETRIES=0
    MAX_RETRIES=10
    while [ $RETRIES -lt $MAX_RETRIES ]; do
        if check_port $BACKEND_PORT; then
            echo -e "${GREEN}   ✅ 后端服务已启动: http://localhost:$BACKEND_PORT${NC}"
            break
        fi
        sleep 1
        RETRIES=$((RETRIES + 1))
    done
    
    if [ $RETRIES -eq $MAX_RETRIES ]; then
        echo -e "${RED}   ❌ 后端服务启动失败${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    
    echo ""
fi

# 启动前端
if [ "$BACKEND_ONLY" = false ]; then
    echo -e "${GREEN}🚀 正在启动前端服务...${NC}"
    
    FRONTEND_PATH="$PROJECT_ROOT/frontend"
    
    if [ ! -d "$FRONTEND_PATH" ]; then
        echo -e "${RED}❌ 前端目录不存在: $FRONTEND_PATH${NC}"
        exit 1
    fi
    
    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ 未找到 Node.js，请安装 Node.js 20+${NC}"
        exit 1
    fi
    
    echo -e "${GRAY}   Node.js: $(which node)${NC}"
    
    # 检查 npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ 未找到 npm${NC}"
        exit 1
    fi
    
    # 检查 node_modules
    if [ ! -d "$FRONTEND_PATH/node_modules" ]; then
        echo -e "${YELLOW}   安装前端依赖...${NC}"
        cd "$FRONTEND_PATH"
        npm install
    fi
    
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${GREEN}  🎉 所有服务已启动！${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    echo -e "${WHITE}  📊 后端 API: http://localhost:$BACKEND_PORT${NC}"
    echo -e "${WHITE}  🎨 前端页面: http://localhost:$FRONTEND_PORT${NC}"
    echo ""
    echo -e "${GRAY}  API 接口:${NC}"
    echo -e "${GRAY}    - GET http://localhost:$BACKEND_PORT/api/today-game${NC}"
    echo -e "${GRAY}    - GET http://localhost:$BACKEND_PORT/api/career-stats${NC}"
    echo -e "${GRAY}    - GET http://localhost:$BACKEND_PORT/api/all-stats${NC}"
    echo ""
    echo -e "${YELLOW}  按 Ctrl+C 停止服务${NC}"
    echo ""
    
    # 启动前端（前台运行）
    cd "$FRONTEND_PATH"
    npm run dev
fi

# 如果是仅后端模式
if [ "$BACKEND_ONLY" = true ]; then
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${GREEN}  ✅ 后端服务已启动！${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    echo -e "${WHITE}  📊 后端 API: http://localhost:$BACKEND_PORT${NC}"
    echo ""
    echo -e "${YELLOW}  按 Ctrl+C 停止服务${NC}"
    echo ""
    
    # 等待
    wait
fi
