# 🏀 NBA 詹姆斯数据展示平台 - 项目说明书

**版本**: v1.0  
**更新时间**: 2026-03-29  
**项目位置**: `/home/ubuntu/projects/nba-stats/`

---

## 📋 项目概述

### 项目简介

NBA 詹姆斯数据展示平台是一个全栈应用，提供勒布朗·詹姆斯（LeBron James）的实时比赛数据、生涯统计和历史排名展示。

**核心功能**:
- 📊 今日战报 - 最近一场比赛详细数据
- 📈 生涯统计 - 职业生涯累计数据
- 🏆 历史排名 - NBA 历史排行榜位置

### 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| **后端框架** | FastAPI | 最新 |
| **前端框架** | React + TypeScript | 19 |
| **构建工具** | Vite | 8.0.3 |
| **数据源** | nba_api | 1.11.4 |
| **样式** | Tailwind CSS | 最新 |
| **图标** | lucide-react | 最新 |

### 项目结构

```
nba-stats/
├── backend-delivery/          # 后端 API
│   ├── src/
│   │   ├── main.py           # FastAPI 主程序
│   │   └── nba_data_client.py # NBA 数据客户端
│   ├── docs/                 # 后端文档
│   ├── logs/                 # 日志目录
│   ├── .env.example          # 环境变量示例
│   └── requirements.txt      # Python 依赖
│
├── frontend/                  # 前端 React 应用
│   ├── src/
│   │   ├── App.tsx           # 主页面组件
│   │   ├── api/
│   │   │   └── statsApi.ts   # API 调用封装
│   │   ├── hooks/
│   │   │   └── useStats.ts   # 数据获取 Hook
│   │   └── types/
│   │       └── stats.ts      # TypeScript 类型定义
│   ├── .env                  # 环境变量
│   ├── vite.config.ts        # Vite 配置
│   └── package.json          # Node.js 依赖
│
├── FIX_REPORT.md             # 修复报告
└── README.md                 # 项目说明
```

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.10+
- **Node.js**: 18+
- **npm**: 9+

### 后端启动

```bash
# 进入后端目录
cd /home/ubuntu/projects/nba-stats/backend-delivery

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python src/main.py
```

**访问地址**:
- API 服务：http://localhost:3000
- API 文档：http://localhost:3000/docs

### 前端启动

```bash
# 进入前端目录
cd /home/ubuntu/projects/nba-stats/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**访问地址**:
- 前端页面：http://localhost:5173
- 内网访问：http://10.3.0.14:5173

---

## 📡 API 接口

### 接口列表

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 健康检查 | GET | `/api/health` | 检查 API 状态 |
| 今日战报 | GET | `/api/today-game` | 获取最近比赛数据 |
| 生涯统计 | GET | `/api/career-stats` | 获取生涯累计数据 |
| 批量获取 | GET | `/api/all-stats` | 一次性获取所有数据 |

### 接口详情

#### 1. 健康检查

**请求**:
```http
GET /api/health
```

**响应** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-03-29T23:28:03.686773",
  "api_version": "1.0.0"
}
```

---

#### 2. 今日战报

**请求**:
```http
GET /api/today-game
```

**响应** (200 OK):
```json
{
  "opponent": "篮网",
  "date": "2026-03-28",
  "result": "W",
  "points": 14,
  "rebounds": 6,
  "assists": 8,
  "steals": 1,
  "blocks": 0,
  "minutes": 37.0,
  "fgPercent": 45.5,
  "threePercent": 33.3,
  "ftPercent": 80.0
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| opponent | string | 对手球队名称 |
| date | string | 比赛日期 (YYYY-MM-DD) |
| result | string | 比赛结果 (W=胜，L=负) |
| points | number | 得分 |
| rebounds | number | 篮板 |
| assists | number | 助攻 |
| steals | number | 抢断 |
| blocks | number | 盖帽 |
| minutes | number | 出场时间（分钟） |
| fgPercent | number | 投篮命中率 (%) |
| threePercent | number | 三分命中率 (%) |
| ftPercent | number | 罚球命中率 (%) |

---

#### 3. 生涯统计

**请求**:
```http
GET /api/career-stats
```

**响应** (200 OK):
```json
{
  "stats": {
    "games": 1615,
    "points": 43290,
    "rebounds": 12047,
    "assists": 11952,
    "steals": 2405,
    "blocks": 1147,
    "minutes": 59390,
    "tripleDoubles": 122
  },
  "rankings": [
    {
      "category": "总得分",
      "careerValue": 43290,
      "rank": 1,
      "prevPlayerName": "贾巴尔",
      "prevPlayerValue": 38387,
      "gapToPrev": 4903
    },
    {
      "category": "总助攻",
      "careerValue": 11952,
      "rank": 4,
      "prevPlayerName": "纳什",
      "prevPlayerValue": 10335,
      "gapToPrev": 1617
    }
  ]
}
```

**stats 字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| games | number | 出场次数 |
| points | number | 总得分 |
| rebounds | number | 总篮板 |
| assists | number | 总助攻 |
| steals | number | 总抢断 |
| blocks | number | 总盖帽 |
| minutes | number | 总出场时间（分钟） |
| tripleDoubles | number | 三双次数 |

**rankings 字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| category | string | 统计类别 |
| careerValue | number | 生涯累计值 |
| rank | number | 历史排名 |
| prevPlayerName | string | 上一名球员姓名 |
| prevPlayerValue | number | 上一名球员数据 |
| gapToPrev | number | 与上一名差距（正=领先，负=落后） |

---

#### 4. 批量获取

**请求**:
```http
GET /api/all-stats
```

**响应** (200 OK):
```json
{
  "todayGame": {
    "opponent": "篮网",
    "date": "2026-03-28",
    "result": "W",
    "points": 14,
    ...
  },
  "career": {
    "stats": {
      "games": 1615,
      "points": 43290,
      ...
    },
    "rankings": [...]
  }
}
```

**说明**: 一次性返回今日战报和生涯统计，减少前端请求次数。

---

## 🔧 配置说明

### 后端配置

**文件**: `backend-delivery/.env.example`

```bash
# CORS 允许的源（逗号分隔）
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# 日志级别
LOG_LEVEL=INFO
```

### 前端配置

**文件**: `frontend/.env`

```bash
# API 基础 URL（开发环境使用 Vite 代理）
VITE_API_BASE_URL=/api

# 生产环境配置
# VITE_API_BASE_URL=https://api.yourdomain.com/api
```

---

## 📊 数据说明

### 数据来源

- **比赛数据**: NBA 官方 API（通过 nba_api 库）
- **生涯统计**: NBA 官方历史数据
- **历史排名**: NBA 历史排行榜

### 数据更新频率

| 数据类型 | 更新频率 | 说明 |
|----------|----------|------|
| 今日战报 | 每场比赛后 | 自动更新 |
| 生涯统计 | 每场比赛后 | 自动累加 |
| 历史排名 | 实时计算 | 基于生涯数据 |

### 当前数据（截至 2026-03-28）

**生涯累计**:
- 出场：1,615 场 🥇 历史第 1
- 得分：43,290 分 🥇 历史第 1
- 篮板：12,047 个
- 助攻：11,952 次
- 抢断：2,405 次

---

## 🐛 故障排除

### 后端问题

**问题**: API 服务无法启动

**解决**:
```bash
# 检查 Python 版本
python3 --version  # 需要 3.10+

# 重新安装依赖
pip install -r requirements.txt

# 查看日志
tail -f logs/api.log
```

**问题**: nba_api 导入失败

**解决**:
```bash
# 检查 nba_api 版本
pip show nba_api

# 重新安装
pip install --upgrade nba_api
```

### 前端问题

**问题**: 页面显示空白

**解决**:
```bash
# 清除缓存
rm -rf node_modules/.vite

# 重启开发服务器
npm run dev -- --force
```

**问题**: API 请求失败

**解决**:
```bash
# 检查后端服务
curl http://localhost:3000/api/health

# 检查 Vite 代理配置
cat vite.config.ts
```

---

## 📝 开发日志

### 2026-03-29

- ✅ 完成前后端对接
- ✅ 修复 10 个代码问题（P0+P1）
- ✅ 代码质量提升至 86/100
- ✅ 修复前端图标问题
- ✅ 完成项目文档整理

---

## 🔗 相关链接

- **NBA 官网**: https://www.nba.com
- **nba_api 文档**: https://github.com/swar/nba_api
- **FastAPI 文档**: https://fastapi.tiangolo.com
- **React 文档**: https://react.dev

---

**文档版本**: v1.0  
**最后更新**: 2026-03-29 23:30  
**维护者**: 小海螺
