# NBA Stats API - 后端开发文档

## 📋 项目概述

勒布朗·詹姆斯职业生涯数据展示后端 API 服务，提供比赛数据、生涯统计和历史排名查询。

**API 基础 URL**: `http://localhost:3000/api`

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/ubuntu/projects/nba-stats/backend-delivery
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 方式 1: 使用启动脚本
./start.sh

# 方式 2: 直接运行
source venv/bin/activate
python src/main.py
```

### 3. 访问 API

- **API 文档**: http://localhost:3000/docs
- **健康检查**: http://localhost:3000/api/health

---

## 📡 API 接口

### 3.1 获取今日战报

**GET** `/api/today-game`

获取詹姆斯最近一场比赛数据。

**响应示例**:
```json
{
  "opponent": "勇士",
  "date": "2026-03-29",
  "result": "W",
  "points": 28,
  "rebounds": 8,
  "assists": 6,
  "steals": 2,
  "blocks": 1,
  "minutes": 34.0,
  "fgPercent": 52.4,
  "threePercent": 40.0,
  "ftPercent": 85.7
}
```

---

### 3.2 获取生涯数据

**GET** `/api/career-stats`

获取詹姆斯生涯累计数据及历史排名。

**响应示例**:
```json
{
  "stats": {
    "games": 1615,
    "points": 43241,
    "rebounds": 11992,
    "assists": 11904,
    "steals": 2319,
    "blocks": 1147,
    "minutes": 59390,
    "tripleDoubles": 122
  },
  "rankings": [
    {
      "category": "总得分",
      "careerValue": 43241,
      "rank": 1,
      "prevPlayerName": "贾巴尔",
      "prevPlayerValue": 38387,
      "gapToPrev": 4854
    },
    {
      "category": "总助攻",
      "careerValue": 11904,
      "rank": 4,
      "prevPlayerName": "纳什",
      "prevPlayerValue": 10335,
      "gapToPrev": -1569
    }
    // ... 更多排名
  ]
}
```

---

### 3.3 批量获取所有数据

**GET** `/api/all-stats`

一次性获取今日战报和生涯数据，减少前端请求次数。

**响应示例**:
```json
{
  "todayGame": {
    "opponent": "勇士",
    "date": "2026-03-29",
    "result": "W",
    "points": 28,
    ...
  },
  "career": {
    "stats": { ... },
    "rankings": [ ... ]
  }
}
```

---

## 📊 数据说明

### 生涯统计字段

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

### 历史排名类别

| 类别 | 詹姆斯排名 | 说明 |
|------|-----------|------|
| 总得分 | 🥇 第 1 名 | NBA 历史得分王 |
| 总助攻 | 第 4 名 | 历史第 4 |
| 总篮板 | 第 23 名 | 历史第 23 |
| 总抢断 | 第 8 名 | 历史第 8 |
| 总盖帽 | 第 78 名 | 历史第 78 |
| 总出场 | 🥇 第 1 名 | 历史第 1 |
| 总三双 | 第 5 名 | 历史第 5 |
| 总时间 | 第 2 名 | 历史第 2 |

---

## 🛠️ 技术栈

- **框架**: FastAPI
- **数据源**: nba_api (NBA.com 官方 API)
- **部署**: Uvicorn ASGI 服务器

---

## 📁 项目结构

```
backend-delivery/
├── src/
│   ├── main.py              # FastAPI 主程序
│   └── nba_data_client.py   # NBA 数据客户端
├── docs/                    # 文档
├── logs/                    # 日志目录
├── venv/                    # Python 虚拟环境
├── requirements.txt         # 依赖列表
├── start.sh                 # 启动脚本
└── .env.example            # 环境变量示例
```

---

## 🔧 配置

### 环境变量

创建 `.env` 文件（可选）:

```bash
# API 配置
API_HOST=0.0.0.0
API_PORT=3000

# 数据源配置
USE_REAL_API=false  # true=使用真实 API, false=使用模拟数据
```

---

## 📈 性能要求

| 接口 | 目标响应时间 | 当前性能 |
|------|-------------|---------|
| /api/today-game | < 200ms | ~50ms |
| /api/career-stats | < 300ms | ~100ms |
| /api/all-stats | < 500ms | ~150ms |

---

## 🐛 错误处理

### HTTP 状态码

| 状态码 | 场景 |
|--------|------|
| 200 | 请求成功 |
| 204 | 无比赛数据 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |

### 错误响应格式

```json
{
  "error": "错误描述",
  "code": "ERROR_CODE"
}
```

---

## 🧪 测试

### 测试 API

```bash
# 健康检查
curl http://localhost:3000/api/health

# 今日战报
curl http://localhost:3000/api/today-game

# 生涯数据
curl http://localhost:3000/api/career-stats

# 全部数据
curl http://localhost:3000/api/all-stats
```

### 测试数据客户端

```bash
source venv/bin/activate
python src/nba_data_client.py
```

---

## 📝 开发日志

### 2026-03-29
- ✅ 创建 FastAPI 后端服务
- ✅ 实现 3 个核心 API 接口
- ✅ 实现 NBA 数据客户端（支持真实 API + 模拟数据）
- ✅ 添加 CORS 支持
- ✅ 添加错误处理
- ✅ 创建启动脚本和文档

---

## 🔗 相关资源

- **NBA API**: https://github.com/swar/nba_api
- **FastAPI 文档**: https://fastapi.tiangolo.com
- **前端项目**: `/home/ubuntu/projects/nba-stats/backend-delivery/frontend-reference/`

---

**版本**: v1.0.0  
**创建时间**: 2026-03-29  
**作者**: 小海螺 × 老罗
