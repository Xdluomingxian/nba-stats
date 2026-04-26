# LeBron James 数据展示 - 完整全栈项目

一个展示 LeBron James（勒布朗·詹姆斯）职业生涯数据的现代化全栈应用。

## 🏀 项目简介

本项目整合了：
- **前端**：美观的 React + TypeScript + Tailwind CSS 界面（Lakers紫金主题）
- **后端**：FastAPI + nba_api 实时获取NBA官方数据
- **数据**：真实比赛数据 + 生涯统计 + 历史排名

## 📁 项目结构

```
lebron-stats-fullstack/
├── 📁 frontend/          # 前端项目 (React + Vite)
│   ├── src/
│   │   ├── pages/       # PC端和移动端页面
│   │   ├── hooks/       # 数据获取Hooks
│   │   ├── components/ui/  # 50+ UI组件
│   │   └── api/         # API接口
│   ├── public/images/   # 静态资源
│   └── package.json
│
├── 📁 backend/          # 后端项目 (FastAPI)
│   ├── main.py          # API入口
│   ├── nba_data_client.py  # NBA数据客户端
│   ├── data/            # 数据文件
│   └── requirements.txt
│
├── 📁 scripts/          # 启动脚本
│   ├── start-backend.ps1    # Windows后端启动
│   ├── start-frontend.ps1   # Windows前端启动
│   └── start-all.ps1        # Windows一键启动
│
├── 📄 README.md         # 项目说明
└── 📄 .env              # 环境变量配置
```

## 🚀 快速开始

### 方式一：手动启动

#### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# macOS/Linux 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python main.py
```

后端服务将在 http://localhost:3000 启动

#### 2. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

### 方式二：使用脚本一键启动（Windows）

```powershell
# 使用 PowerShell
.\scripts\start-all.ps1
```

## 🔧 环境变量配置

### 后端环境变量（backend/.env）

```bash
# CORS允许的前端地址（多个用逗号分隔）
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# 可选：NBA API相关配置
NBA_API_TIMEOUT=30
```

### 前端环境变量（frontend/.env）

```bash
# 使用真实API（false）或Mock数据（true）
VITE_USE_MOCK=false

# 后端API地址
VITE_API_BASE_URL=http://localhost:3000/api
```

## 📊 API接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 今日战报 | GET | `/api/today-game` | 获取最近一场比赛数据 |
| 生涯统计 | GET | `/api/career-stats` | 获取生涯累计数据及排名 |
| 批量获取 | GET | `/api/all-stats` | 一次性获取所有数据 |
| 健康检查 | GET | `/api/health` | 服务健康状态 |

## 🎨 功能特性

### 前端
- ✅ 响应式设计（PC端 + 移动端）
- ✅ Lakers紫金主题配色
- ✅ 实时数据展示（今日战报 + 生涯累计）
- ✅ 历史排名对比
- ✅ 自动5分钟刷新
- ✅ 50+ shadcn/ui 组件
- ✅ Mock/真实API切换

### 后端
- ✅ FastAPI高性能框架
- ✅ 对接NBA官方API (nba_api)
- ✅ 自动回退Mock数据
- ✅ CORS跨域支持
- ✅ 详细的日志记录
- ✅ 错误处理机制

## 📱 截图预览

**PC端**：16:10海报式布局，左侧球员图片 + 右侧数据面板  
**移动端**：Tab切换（今日战报 / 生涯累计），顶部横幅

## 🛠️ 技术栈

### 前端
- React 19 + TypeScript
- Vite 7
- Tailwind CSS 3.4
- Radix UI + shadcn/ui
- Recharts（图表）

### 后端
- Python 3.8+
- FastAPI
- nba_api
- Uvicorn
- Pandas

## 📝 更新日志

### v1.1.0 (2026-04-02)
- **API优化**：修复NBA API调用错误（PlayerGameLog、AllTimeLeadersGrids参数修正）
- **智能缓存**：实现多级缓存机制（比赛数据1小时、生涯数据24小时、排名数据7天）
- **智能刷新**：比赛日智能刷新，非比赛日使用缓存，大幅减少API调用
- **时区感知**：根据访问者IP自动显示本地时区日期（中国用户显示北京时间）
- **局域网支持**：前端支持局域网访问，Vite代理转发API请求
- **数据验证**：调用API前验证数据一致性，确保显示真实数据
- **赛季修正**：修正赛季配置为2024-25赛季

### v1.0.0 (2026-04-01)
- 整合前端和后端项目
- 支持真实NBA数据API
- 完善的错误处理和日志
- 一键启动脚本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**致敬传奇** 👑  
*The King - LeBron James*
