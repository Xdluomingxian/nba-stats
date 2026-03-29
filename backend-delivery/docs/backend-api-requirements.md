# LeBron James 数据展示 - 后端API开发需求文档

## 1. 项目概述

### 1.1 项目背景
开发一个LeBron James（勒布朗·詹姆斯）职业生涯数据展示页面，包含：
- **今日战报**：展示最近一场比赛的详细数据
- **生涯累计**：常规赛生涯统计数据
- **历史排名**：各项数据在NBA历史排行榜中的位置

### 1.2 前端技术栈
- **框架**：React 19 + TypeScript
- **构建工具**：Vite 7
- **UI组件**：Radix UI + Tailwind CSS
- **图表**：Recharts

### 1.3 API基础配置
```typescript
const API_BASE_URL = 'http://localhost:3000/api';
```

---

## 2. API接口规范

### 2.1 接口清单

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 今日战报 | GET | `/api/today-game` | 获取最近一场比赛数据 |
| 生涯统计 | GET | `/api/career-stats` | 获取生涯累计数据及排名 |
| 批量获取 | GET | `/api/all-stats` | 一次性获取所有数据 |

### 2.2 详细接口定义

#### 2.2.1 获取今日战报

**请求**
```http
GET /api/today-game
Content-Type: application/json
```

**响应成功 (200)**
```typescript
{
  "opponent": "string",      // 对手球队名称，如"勇士"
  "date": "string",          // 比赛日期，格式：YYYY-MM-DD
  "result": "string",        // 比赛结果："W" (胜) 或 "L" (负)
  "points": number,          // 得分
  "rebounds": number,        // 篮板
  "assists": number,         // 助攻
  "steals": number,          // 抢断
  "blocks": number,          // 盖帽
  "minutes": number,         // 出场时间（分钟）
  "fgPercent": number,       // 投篮命中率（百分比，如52.4）
  "threePercent": number,    // 三分命中率
  "ftPercent": number        // 罚球命中率
}
```

**响应示例**
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

**特殊情况**
- 无比赛日（休赛期/全明星周末）：返回 `null` 或 `204 No Content`

---

#### 2.2.2 获取生涯统计数据

**请求**
```http
GET /api/career-stats
Content-Type: application/json
```

**响应成功 (200)**
```typescript
{
  "stats": {
    "games": number,          // 出场次数
    "points": number,         // 总得分
    "rebounds": number,       // 总篮板
    "assists": number,        // 总助攻
    "steals": number,         // 总抢断
    "blocks": number,         // 总盖帽
    "minutes": number,        // 总出场时间（分钟）
    "tripleDoubles": number   // 三双次数
  },
  "rankings": [
    {
      "category": "string",      // 统计类别，如"总得分"
      "careerValue": number,     // 生涯累计值
      "rank": number,            // 历史排名
      "prevPlayerName": "string", // 上一名球员（排名更高的那位）
      "prevPlayerValue": number, // 上一名球员的数据
      "gapToPrev": number        // 与上一名的差距（正值为领先，负值为落后）
    }
  ]
}
```

**响应示例**
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
  ]
}
```

**排名类别（必须包含）**
| 类别 | 说明 |
|------|------|
| 总得分 | Points |
| 总助攻 | Assists |
| 总篮板 | Rebounds |
| 总抢断 | Steals |
| 总盖帽 | Blocks |
| 总出场 | Games Played |
| 总三双 | Triple-doubles |
| 总时间 | Minutes |

---

#### 2.2.3 批量获取所有数据

**请求**
```http
GET /api/all-stats
Content-Type: application/json
```

**响应成功 (200)**
```typescript
{
  "todayGame": {
    // TodayGameStats 对象（同 /api/today-game）
  },
  "career": {
    "stats": {
      // CareerStats 对象
    },
    "rankings": [
      // RankingData[] 数组
    ]
  }
}
```

**用途**：减少前端请求次数，提升加载性能

---

## 3. TypeScript 接口定义

### 3.1 前端数据结构（供后端参考）

```typescript
// ==================== 数据类型定义 ====================

/**
 * 今日战报数据
 * 对应最近一场比赛的详细统计
 */
export interface TodayGameStats {
  /** 对手球队名称 */
  opponent: string;
  /** 比赛日期，格式：YYYY-MM-DD */
  date: string;
  /** 比赛结果：W=胜利，L=失败 */
  result: 'W' | 'L';
  /** 得分 */
  points: number;
  /** 篮板 */
  rebounds: number;
  /** 助攻 */
  assists: number;
  /** 抢断 */
  steals: number;
  /** 盖帽 */
  blocks: number;
  /** 出场时间（分钟） */
  minutes: number;
  /** 投篮命中率（百分比数值，如52.4表示52.4%） */
  fgPercent: number;
  /** 三分命中率 */
  threePercent: number;
  /** 罚球命中率 */
  ftPercent: number;
}

/**
 * 生涯累计数据
 * 常规赛生涯统计数据
 */
export interface CareerStats {
  /** 出场次数 */
  games: number;
  /** 总得分 */
  points: number;
  /** 总篮板 */
  rebounds: number;
  /** 总助攻 */
  assists: number;
  /** 总抢断 */
  steals: number;
  /** 总盖帽 */
  blocks: number;
  /** 总出场时间（分钟） */
  minutes: number;
  /** 三双次数 */
  tripleDoubles: number;
}

/**
 * 历史排名数据
 * 某一项统计数据的历史排名信息
 */
export interface RankingData {
  /** 统计类别名称 */
  category: string;
  /** 生涯累计值 */
  careerValue: number;
  /** 历史排名（1表示历史第一） */
  rank: number;
  /** 上一名球员（排名更高的那位）名称 */
  prevPlayerName: string;
  /** 上一名球员的数据值 */
  prevPlayerValue: number;
  /** 
   * 与上一名的差距
   * - 正值：领先下一名的数值（如 rank=1 时）
   * - 负值：距离上一名的差距（如 rank>1 时）
   */
  gapToPrev: number;
}

// ==================== API 响应类型 ====================

/**
 * /api/today-game 响应
 */
export type TodayGameResponse = TodayGameStats | null;

/**
 * /api/career-stats 响应
 */
export interface CareerStatsResponse {
  stats: CareerStats;
  rankings: RankingData[];
}

/**
 * /api/all-stats 响应
 */
export interface AllStatsResponse {
  todayGame: TodayGameStats | null;
  career: {
    stats: CareerStats;
    rankings: RankingData[];
  };
}
```

---

## 4. 错误处理规范

### 4.1 HTTP状态码

| 状态码 | 场景 | 响应体 |
|--------|------|--------|
| 200 | 请求成功 | 数据对象 |
| 204 | 无比赛日 | 空响应 |
| 400 | 请求参数错误 | `{ "error": "Invalid request" }` |
| 500 | 服务器内部错误 | `{ "error": "Internal server error" }` |
| 503 | 数据源不可用（NBA API维护） | `{ "error": "Data source unavailable" }` |

### 4.2 错误响应格式

```typescript
{
  "error": "string",      // 错误描述
  "code": "string",       // 错误码（可选）
  "message": "string"     // 详细错误信息（可选）
}
```

### 4.3 常见错误场景

```json
// 数据源不可用
{
  "error": "Data source unavailable",
  "message": "NBA Stats API is currently under maintenance"
}

// 球员数据未找到
{
  "error": "Player not found",
  "message": "LeBron James data is temporarily unavailable"
}

// 服务器内部错误
{
  "error": "Internal server error",
  "message": "Failed to fetch data from external API"
}
```

---

## 5. 性能要求

### 5.1 响应时间

| 接口 | 目标响应时间 | 最大响应时间 |
|------|-------------|-------------|
| /api/today-game | < 200ms | < 500ms |
| /api/career-stats | < 300ms | < 800ms |
| /api/all-stats | < 500ms | < 1000ms |

### 5.2 缓存策略

**建议实现**
- **今日战报**：缓存5分钟（比赛进行中可缩短）
- **生涯统计**：缓存1小时（数据变化频率低）
- **历史排名**：缓存24小时（赛季结束才更新）

**前端缓存**
前端已实现5分钟自动刷新机制（仅真实API模式）

---

## 6. 数据源建议

### 6.1 官方数据源

| 数据源 | URL | 用途 |
|--------|-----|------|
| NBA Stats API | stats.nba.com | 官方比赛数据 |
| Basketball-Reference | basketball-reference.com | 生涯统计数据 |
| ESPN API | espn.com | 比赛结果和实时数据 |

### 6.2 数据采集建议

**实时数据（今日战报）**
- 调用NBA Stats API获取最近比赛
- 比赛结束后更新缓存
- 比赛日每15分钟刷新一次

**历史数据（生涯统计）**
- 赛季开始前批量导入
- 每场比赛后更新累计数据
- 历史排名数据可手动维护（变化频率低）

---

## 7. 环境变量配置

前端通过环境变量控制Mock/真实API切换：

```bash
# .env (开发环境 - 使用Mock数据)
VITE_USE_MOCK=true

# .env (生产环境 - 使用真实API)
VITE_USE_MOCK=false
VITE_API_BASE_URL=https://your-api-domain.com/api
```

---

## 8. 测试建议

### 8.1 Mock数据测试
前端已提供完整的Mock服务，可用于：
- 前端独立开发
- UI/UX测试
- 无网络环境演示

### 8.2 集成测试
建议测试场景：
1. 正常比赛日数据返回
2. 无比赛日（返回null）
3. 网络超时处理
4. 服务器错误处理
5. 缓存刷新机制

---

## 9. 部署检查清单

- [ ] API响应格式符合接口规范
- [ ] 响应时间满足性能要求
- [ ] CORS配置允许前端域名访问
- [ ] 错误处理返回标准格式
- [ ] 日志记录包含请求追踪ID
- [ ] 监控告警配置（响应时间、错误率）
- [ ] 缓存机制已启用
- [ ] 数据源自动降级方案（主源故障时切换备用源）

---

## 10. 联系方式

**前端开发**：负责React应用开发和Mock数据维护  
**后端开发**：负责API开发和数据源集成  
**数据维护**：负责历史排名数据更新和验证

---

*文档版本：v1.0*  
*最后更新：2025-03-29*
