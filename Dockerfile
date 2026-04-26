# 阶段一：构建前端
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# 阶段二：Python 后端
FROM python:3.11-slim AS backend

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ ./

# 复制前端构建产物到后端静态目录
COPY --from=frontend-builder /app/frontend/dist ./static

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
