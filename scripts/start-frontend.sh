#!/bin/bash

# 启动前端服务
# 使用: bash scripts/start-frontend.sh

set -e

# 颜色定义
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  启动 LeBron Stats 前端服务${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

FRONTEND_PORT=5173

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_PATH="$PROJECT_ROOT/frontend"

# 检查前端目录
if [ ! -d "$FRONTEND_PATH" ]; then
    echo -e "${RED}❌ 前端目录不存在: $FRONTEND_PATH${NC}"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 未找到 Node.js，请安装 Node.js 20+${NC}"
    echo -e "${GRAY}   下载地址: https://nodejs.org/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js: $(which node)${NC}"
echo -e "${GRAY}   版本: $(node --version)${NC}"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ 未找到 npm${NC}"
    exit 1
fi

echo -e "${GREEN}✅ npm: $(which npm)${NC}"

# 检查 node_modules
if [ ! -d "$FRONTEND_PATH/node_modules" ]; then
    echo ""
    echo -e "${YELLOW}📦 安装前端依赖...${NC}"
    cd "$FRONTEND_PATH"
    npm install
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 依赖安装失败${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
else
    echo -e "${GREEN}✅ 依赖已安装${NC}"
fi

echo ""
echo -e "${GREEN}🚀 启动前端服务...${NC}"
echo -e "${GRAY}   端口: $FRONTEND_PORT${NC}"
echo -e "${GRAY}   地址: http://localhost:$FRONTEND_PORT${NC}"
echo ""

# 检查 .env 配置
ENV_FILE="$FRONTEND_PATH/.env"
if [ -f "$ENV_FILE" ]; then
    if grep -q "VITE_USE_MOCK=true" "$ENV_FILE"; then
        echo -e "${YELLOW}⚠️  注意: 当前使用 Mock 数据${NC}"
        echo -e "${GRAY}   如需使用真实 API，请修改 .env 文件:${NC}"
        echo -e "${GRAY}   VITE_USE_MOCK=false${NC}"
    else
        echo -e "${GREEN}✅ 使用真实 API 数据${NC}"
    fi
fi

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}  🎨 前端服务已启动！${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${WHITE}  访问地址: http://localhost:$FRONTEND_PORT${NC}"
echo ""
echo -e "${YELLOW}  按 Ctrl+C 停止服务${NC}"
echo ""

# 启动前端
cd "$FRONTEND_PATH"
npm run dev
