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
| 今日战报 | GET | `/api/today-game?season_type=Regular Season\|Playoffs` | 获取最近一场比赛数据 |
| 生涯统计 | GET | `/api/career-stats` | 获取常规赛生涯数据及排名 |
| 季后赛生涯 | GET | `/api/playoff-career-stats` | 获取季后赛生涯数据 |
| 批量获取 | GET | `/api/all-stats?season_type=Regular Season\|Playoffs` | 一次性获取所有数据 |
| 健康检查 | GET | `/api/health` | 服务健康状态 |

## 🎨 功能特性

### 前端
- ✅ 响应式设计（PC端 + 移动端）
- ✅ Lakers紫金主题配色
- ✅ 实时数据展示（今日战报 + 生涯累计）
- ✅ **赛季类型切换**：支持常规赛/季后赛数据切换
- ✅ 历史排名对比
- ✅ 自动刷新（5分钟间隔 + 1分钟本地缓存）
- ✅ 50+ shadcn/ui 组件
- ✅ Mock/真实API切换
- ✅ ErrorBoundary 错误边界保护

### 后端
- ✅ FastAPI高性能框架
- ✅ 对接NBA官方API (nba_api)
- ✅ CORS跨域支持
- ✅ 速率限制（slowapi）
- ✅ 详细的日志记录
- ✅ 错误处理机制
- ✅ 智能缓存（1小时比赛数据、24小时生涯数据、7天排名数据）

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

### v1.2.0 (2026-04-27)
- **季后赛数据支持**：新增 `/api/playoff-career-stats` 接口，支持季后赛生涯数据查询
- **赛季类型切换**：首页新增常规赛/季后赛 Tab 切换，用户可自由查看不同赛季类型数据
- **后端优化**：
  - `today-game` 接口新增 `season_type` 查询参数
  - 比赛数据按赛季类型独立缓存
  - 修复 slowapi 限流中间件参数缺失问题
  - 修复 Windows 环境下 emoji 编码和 GBK 解码问题
- **前端优化**：
  - 修复 `Basketball` 图标不存在导致的页面空白问题
  - 独立 API 请求逻辑，单个接口失败不影响其他数据展示
  - 新增 ErrorBoundary 错误边界，提升容错能力
  - 优化赛季计算逻辑（基于月份自动判断当前赛季）
  - 修复日期解析和排序问题
  - 移除 mock 数据回退，确保数据真实性
- **代码质量**：
  - 添加 `.gitignore` 配置，排除 node_modules、__pycache__、.env 等文件
  - 修复 Git 合并冲突标记残留问题

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
