# NBA数据API接口文档

## 接口概述

本文档定义了勒布朗·詹姆斯数据统计展示页面的后端API接口规范，供后端开发参考实现。

**基础URL**: `http://localhost:3000/api` (开发环境)  
**数据格式**: JSON  
**编码**: UTF-8

---

## 1. 接口列表

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取今日战报 | GET | `/api/today-game` | 获取最近一场比赛的详细数据 |
| 获取生涯数据 | GET | `/api/career-stats` | 获取生涯累计数据及历史排名 |
| 获取全部数据 | GET | `/api/all-stats` | 获取今日战报+生涯数据（合并接口）|

---

## 2. 接口详情

### 2.1 获取今日战报

**请求**
```http
GET /api/today-game
Content-Type: application/json
```

**响应**
```json
{
  "opponent": "勇士",
  "date": "2025-03-28",
  "result": "W",
  "points": 28,
  "rebounds": 8,
  "assists": 6,
  "steals": 2,
  "blocks": 1,
  "minutes": 34,
  "fgPercent": 52.4,
  "threePercent": 40.0,
  "ftPercent": 85.7
}
```

**字段说明**

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| opponent | string | 对手球队名称 | "勇士" |
| date | string | 比赛日期 (YYYY-MM-DD) | "2025-03-28" |
| result | string | 比赛结果，W=胜，L=负 | "W" |
| points | number | 得分 | 28 |
| rebounds | number | 篮板 | 8 |
| assists | number | 助攻 | 6 |
| steals | number | 抢断 | 2 |
| blocks | number | 盖帽 | 1 |
| minutes | number | 出场时间（分钟） | 34 |
| fgPercent | number | 投篮命中率 (%) | 52.4 |
| threePercent | number | 三分命中率 (%) | 40.0 |
| ftPercent | number | 罚球命中率 (%) | 85.7 |

---

### 2.2 获取生涯数据

**请求**
```http
GET /api/career-stats
Content-Type: application/json
```

**响应**
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
      "rank":4,
      "prevPlayerName": "纳什",
      "prevPlayerValue": 10335,
      "gapToPrev": -1569
    }
    // ... 更多排名数据
  ]
}
```

**字段说明 - stats（生涯统计数据）**

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| games | number | 出场数 | 1615 |
| points | number | 总得分 | 43241 |
| rebounds | number | 总篮板 | 11992 |
| assists | number | 总助攻 | 11904 |
| steals | number | 总抢断 | 2319 |
| blocks | number | 总盖帽 | 1147 |
| minutes | number | 总出场时间（分钟） | 59390 |
| tripleDoubles | number | 三双次数 | 122 |

**字段说明 - rankings（历史排名数据）**

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| category | string | 统计类别 | "总得分" |
| careerValue | number | 生涯累计值 | 43241 |
| rank | number | 历史排名 | 1 |
| prevPlayerName | string | 上一名球员（排名更高的那位） | "贾巴尔" |
| prevPlayerValue | number | 上一名球员的数值 | 38387 |
| gapToPrev | number | 与上一名的差距（正数=领先，负数=落后） | 4854 |

**排名数据说明**

`gapToPrev` 字段的含义：
- **正数**：表示领先于上一名（即当前是第1名，领先第2名）
- **负数**：表示落后于上一名（即需要追赶上一名）

**支持的category值**：
- 总得分
- 总助攻
- 总篮板
- 总抢断
- 总盖帽
- 总出场
- 总三双
- 总时间

---

### 2.3 获取全部数据

**请求**
```http
GET /api/all-stats
Content-Type: application/json
```

**响应**
```json
{
  "todayGame": {
    "opponent": "勇士",
    "date": "2025-03-28",
    "result": "W",
    "points": 28,
    "rebounds": 8,
    "assists": 6,
    "steals": 2,
    "blocks": 1,
    "minutes": 34,
    "fgPercent": 52.4,
    "threePercent": 40.0,
    "ftPercent": 85.7
  },
  "career": {
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
      }
      // ... 更多排名数据
    ]
  }
}
```

---

## 3. 错误处理

### 3.1 错误响应格式

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```

### 3.2 HTTP状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 404 | 数据不存在 |
| 500 | 服务器内部错误 |

### 3.3 常见错误码

| 错误码 | 说明 |
|--------|------|
| DATA_NOT_FOUND | 比赛数据不存在（今日无比赛） |
| SERVER_ERROR | 服务器内部错误 |

---

## 4. 数据更新策略

### 4.1 今日战报数据

- **更新时机**：每日比赛结束后
- **更新频率**：每日1次
- **数据来源**：NBA官方API或第三方数据服务

### 4.2 生涯累计数据

- **更新时机**：每场比赛后自动累加
- **更新频率**：实时或每日
- **数据存储**：建议持久化存储，支持历史查询

### 4.3 历史排名数据

- **更新时机**：生涯数据变化时重新计算
- **更新频率**：每次比赛后
- **数据来源**：需要维护一个历史排名数据库

---

## 5. 前端使用示例

### 5.1 环境变量配置

在项目根目录创建 `.env` 文件：

```bash
VITE_API_BASE_URL=http://localhost:3000/api
```

### 5.2 数据获取示例

```typescript
import { useStats } from '@/hooks/useStats';

function App() {
  const { todayGame, careerStats, rankings, loading, error, refetch } = useStats();

  if (loading) return <div>加载中...</div>;
  if (error) return <div>错误: {error}</div>;

  return (
    <div>
      <h1>今日得分: {todayGame?.points}</h1>
      <h2>生涯得分: {careerStats?.points}</h2>
    </div>
  );
}
```

---

## 6. 示例数据结构

### 6.1 今日战报 - 完整示例

```json
{
  "opponent": "勇士",
  "date": "2025-03-28",
  "result": "W",
  "points": 28,
  "rebounds": 8,
  "assists": 6,
  "steals": 2,
  "blocks": 1,
  "minutes": 34,
  "fgPercent": 52.4,
  "threePercent": 40.0,
  "ftPercent": 85.7
}
```

### 6.2 生涯数据 - 完整示例

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
    { "category": "总得分", "careerValue": 43241, "rank": 1, "prevPlayerName": "贾巴尔", "prevPlayerValue": 38387, "gapToPrev": 4854 },
    { "category": "总助攻", "careerValue": 11904, "rank": 4, "prevPlayerName": "纳什", "prevPlayerValue": 10335, "gapToPrev": -1569 },
    { "category": "总篮板", "careerValue": 11992, "rank": 23, "prevPlayerName": "瑟蒙德", "prevPlayerValue": 14464, "gapToPrev": -2472 },
    { "category": "总抢断", "careerValue": 2319, "rank": 8, "prevPlayerName": "奇克斯", "prevPlayerValue": 2310, "gapToPrev": 9 },
    { "category": "总盖帽", "careerValue": 1147, "rank": 78, "prevPlayerName": "吉尔摩尔", "prevPlayerValue": 1178, "gapToPrev": -31 },
    { "category": "总出场", "careerValue": 1615, "rank": 1, "prevPlayerName": "帕里什", "prevPlayerValue": 1611, "gapToPrev": 4 },
    { "category": "总三双", "careerValue": 122, "rank": 5, "prevPlayerName": "伯德", "prevPlayerValue": 59, "gapToPrev": 63 },
    { "category": "总时间", "careerValue": 59390, "rank": 2, "prevPlayerName": "贾巴尔", "prevPlayerValue": 66298, "gapToPrev": -6908 }
  ]
}
```

---

## 7. 技术实现建议

### 7.1 后端技术栈推荐
- Node.js + Express
- Python + FastAPI
- Go + Gin

### 7.2 数据存储
- PostgreSQL / MySQL：存储生涯累计数据
- Redis：缓存今日战报数据
- 定时任务：每日比赛后更新数据

### 7.3 数据来源
- NBA官方API (stats.nba.com)
- 第三方数据服务（如 SportsRadar、ESPN API）
- 手动录入（备用方案）

---

**文档版本**: v1.0  
**最后更新**: 2025-03-29
