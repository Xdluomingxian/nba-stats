# 📡 NBA 詹姆斯数据平台 - API 接口文档

**版本**: v1.0  
**基础 URL**: `http://localhost:3000/api`  
**文档更新**: 2026-03-29

---

## 📋 目录

1. [接口概览](#接口概览)
2. [通用说明](#通用说明)
3. [接口详情](#接口详情)
4. [错误码说明](#错误码说明)
5. [前端调用示例](#前端调用示例)
6. [调试工具](#调试工具)

---

## 接口概览

| 接口名称 | 方法 | 路径 | 描述 | 认证 |
|---------|------|------|------|------|
| 健康检查 | GET | `/health` | 检查 API 运行状态 | ❌ |
| 今日战报 | GET | `/today-game` | 获取最近一场比赛数据 | ❌ |
| 生涯统计 | GET | `/career-stats` | 获取生涯累计数据和排名 | ❌ |
| 批量获取 | GET | `/all-stats` | 一次性获取所有数据 | ❌ |

---

## 通用说明

### 请求格式

- **Content-Type**: `application/json`
- **字符编码**: `UTF-8`

### 响应格式

所有接口返回统一的 JSON 格式：

**成功响应**:
```json
{
  "status": "success",
  "data": { ... }
}
```

**错误响应**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述信息"
  }
}
```

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 204 | 无数据（如无比赛） |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |
| 503 | 数据源不可用 |

---

## 接口详情

### 1. 健康检查

检查 API 服务是否正常运行。

#### 请求

```http
GET /api/health
```

#### 响应

**200 OK**:
```json
{
  "status": "healthy",
  "timestamp": "2026-03-29T23:28:03.686773",
  "api_version": "1.0.0"
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | 服务状态 (healthy/unhealthy) |
| timestamp | string | 当前时间戳 (ISO 8601) |
| api_version | string | API 版本号 |

#### cURL 示例

```bash
curl -X GET http://localhost:3000/api/health
```

---

### 2. 今日战报

获取勒布朗·詹姆斯最近一场比赛的详细统计数据。

#### 请求

```http
GET /api/today-game
```

#### 响应

**200 OK**:
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

**204 No Content** (无比赛时):
```json
null
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| opponent | string | ✅ | 对手球队名称 | "篮网" |
| date | string | ✅ | 比赛日期 | "2026-03-28" |
| result | string | ✅ | 比赛结果 | "W" (胜) / "L" (负) |
| points | number | ✅ | 得分 | 14 |
| rebounds | number | ✅ | 篮板 | 6 |
| assists | number | ✅ | 助攻 | 8 |
| steals | number | ✅ | 抢断 | 1 |
| blocks | number | ✅ | 盖帽 | 0 |
| minutes | number | ✅ | 出场时间（分钟） | 37.0 |
| fgPercent | number | ✅ | 投篮命中率 | 45.5 |
| threePercent | number | ✅ | 三分命中率 | 33.3 |
| ftPercent | number | ✅ | 罚球命中率 | 80.0 |

#### cURL 示例

```bash
curl -X GET http://localhost:3000/api/today-game
```

#### JavaScript 示例

```typescript
async function getTodayGame() {
  const response = await fetch('/api/today-game');
  
  if (response.status === 204) {
    return null; // 无比赛
  }
  
  const data = await response.json();
  return data;
}
```

---

### 3. 生涯统计

获取勒布朗·詹姆斯职业生涯累计统计数据和 NBA 历史排名。

#### 请求

```http
GET /api/career-stats
```

#### 响应

**200 OK**:
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
    },
    {
      "category": "总篮板",
      "careerValue": 12047,
      "rank": 23,
      "prevPlayerName": "瑟蒙德",
      "prevPlayerValue": 14464,
      "gapToPrev": -2417
    },
    {
      "category": "总抢断",
      "careerValue": 2405,
      "rank": 8,
      "prevPlayerName": "奇克斯",
      "prevPlayerValue": 2310,
      "gapToPrev": 95
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
| rank | number | 历史排名（1=第 1） |
| prevPlayerName | string | 上一名球员姓名 |
| prevPlayerValue | number | 上一名球员数据 |
| gapToPrev | number | 与上一名差距（正=领先，负=落后） |

**支持的统计类别**:
- 总得分
- 总助攻
- 总篮板
- 总抢断
- 总盖帽
- 总出场
- 总三双
- 总时间

#### cURL 示例

```bash
curl -X GET http://localhost:3000/api/career-stats
```

#### JavaScript 示例

```typescript
async function getCareerStats() {
  const response = await fetch('/api/career-stats');
  const data = await response.json();
  
  console.log('总得分:', data.stats.points);
  console.log('历史排名:', data.rankings);
  
  return data;
}
```

---

### 4. 批量获取

一次性获取今日战报和生涯统计数据，减少 HTTP 请求次数。

#### 请求

```http
GET /api/all-stats
```

#### 响应

**200 OK**:
```json
{
  "todayGame": {
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
  },
  "career": {
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
      }
      // ... 更多排名
    ]
  }
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| todayGame | object | 今日战报数据（同 `/today-game`） |
| career.stats | object | 生涯统计数据（同 `/career-stats`） |
| career.rankings | array | 历史排名数据（同 `/career-stats`） |

#### cURL 示例

```bash
curl -X GET http://localhost:3000/api/all-stats
```

#### JavaScript 示例

```typescript
async function getAllStats() {
  const response = await fetch('/api/all-stats');
  const data = await response.json();
  
  console.log('今日得分:', data.todayGame.points);
  console.log('生涯总分:', data.career.stats.points);
  
  return data;
}
```

---

## 错误码说明

### 通用错误

| 错误码 | HTTP 状态码 | 说明 |
|--------|-----------|------|
| HTTP_400 | 400 | 请求参数错误 |
| HTTP_404 | 404 | 资源不存在 |
| HTTP_500 | 500 | 服务器内部错误 |
| INTERNAL_SERVER_ERROR | 500 | 通用服务器错误 |

### 业务错误

| 错误码 | HTTP 状态码 | 说明 |
|--------|-----------|------|
| DATA_NOT_FOUND | 404 | 数据不存在（如无比赛） |
| PLAYER_NOT_FOUND | 404 | 球员数据未找到 |
| API_UNAVAILABLE | 503 | 数据源不可用 |

### 错误响应示例

```json
{
  "error": {
    "code": "DATA_NOT_FOUND",
    "message": "今日无比赛数据"
  }
}
```

---

## 前端调用示例

### TypeScript 封装

```typescript
// types/stats.ts
export interface TodayGameStats {
  opponent: string;
  date: string;
  result: 'W' | 'L';
  points: number;
  rebounds: number;
  assists: number;
  steals: number;
  blocks: number;
  minutes: number;
  fgPercent: number;
  threePercent: number;
  ftPercent: number;
}

export interface CareerStats {
  games: number;
  points: number;
  rebounds: number;
  assists: number;
  steals: number;
  blocks: number;
  minutes: number;
  tripleDoubles: number;
}

export interface RankingData {
  category: string;
  careerValue: number;
  rank: number;
  prevPlayerName: string;
  prevPlayerValue: number;
  gapToPrev: number;
}

export interface AllStatsResponse {
  todayGame: TodayGameStats | null;
  career: {
    stats: CareerStats;
    rankings: RankingData[];
  };
}

// api/statsApi.ts
const API_BASE_URL = '/api';

export async function fetchAllStats(): Promise<AllStatsResponse> {
  const response = await fetch(`${API_BASE_URL}/all-stats`);
  
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  
  return await response.json();
}

// hooks/useStats.ts
export function useStats() {
  const [data, setData] = useState<AllStatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAllStats()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}
```

### React 组件使用

```typescript
function StatsCard() {
  const { data, loading, error } = useStats();

  if (loading) return <div>加载中...</div>;
  if (error) return <div>错误：{error}</div>;

  return (
    <div>
      <h2>今日战报</h2>
      <p>对手：{data.todayGame.opponent}</p>
      <p>得分：{data.todayGame.points}</p>
      
      <h2>生涯统计</h2>
      <p>总得分：{data.career.stats.points}</p>
      <p>历史排名：第{data.career.rankings[0].rank}名</p>
    </div>
  );
}
```

---

## 调试工具

### 1. Swagger UI

访问：http://localhost:3000/docs

- 在线测试所有接口
- 查看请求/响应格式
- 自动生成客户端代码

### 2. cURL 命令

```bash
# 健康检查
curl http://localhost:3000/api/health

# 今日战报
curl http://localhost:3000/api/today-game

# 生涯统计
curl http://localhost:3000/api/career-stats

# 批量获取
curl http://localhost:3000/api/all-stats
```

### 3. Postman

导入集合：

```json
{
  "info": {
    "name": "NBA Stats API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "健康检查",
      "request": {
        "method": "GET",
        "url": "http://localhost:3000/api/health"
      }
    },
    {
      "name": "今日战报",
      "request": {
        "method": "GET",
        "url": "http://localhost:3000/api/today-game"
      }
    },
    {
      "name": "生涯统计",
      "request": {
        "method": "GET",
        "url": "http://localhost:3000/api/career-stats"
      }
    },
    {
      "name": "批量获取",
      "request": {
        "method": "GET",
        "url": "http://localhost:3000/api/all-stats"
      }
    }
  ]
}
```

### 4. 浏览器开发者工具

```javascript
// 在浏览器控制台执行
fetch('/api/all-stats')
  .then(res => res.json())
  .then(data => console.table(data));
```

---

## 📝 更新日志

### v1.0 (2026-03-29)

- ✅ 初始版本发布
- ✅ 4 个核心接口
- ✅ 完整文档
- ✅ TypeScript 类型定义
- ✅ 前端调用示例

---

**文档维护**: 小海螺  
**联系方式**: 内部通讯  
**最后更新**: 2026-03-29 23:35
