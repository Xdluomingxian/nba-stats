# LeBron James 数据展示项目 - 完整需求规格说明书

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | LeBron Stats - 勒布朗·詹姆斯数据展示系统 |
| 版本 | v1.1.0 |
| 创建日期 | 2026-04-01 |
| 最后更新 | 2026-04-02 |
| 文档类型 | 需求规格说明书 (SRS) |

---

## 目录

1. [项目概述](#1-项目概述)
2. [功能需求](#2-功能需求)
3. [技术架构](#3-技术架构)
4. [数据规范](#4-数据规范)
5. [接口规范](#5-接口规范)
6. [UI/UX设计规范](#6-uiux设计规范)
7. [非功能需求](#7-非功能需求)
8. [开发规范](#8-开发规范)
9. [部署规范](#9-部署规范)
10. [测试策略](#10-测试策略)

---

## 1. 项目概述

### 1.1 项目背景

LeBron James（勒布朗·詹姆斯）是NBA历史上最伟大的球员之一，拥有众多令人瞩目的职业成就：

- **历史得分王**：生涯总得分超过43,000分
- **4届NBA总冠军**：热火2次、骑士1次、湖人1次
- **4次常规赛MVP**：2009、2010、2012、2013
- **21次全明星**：历史第一
- **历史出场王**：常规赛出场数历史第一

本项目旨在通过现代化的Web技术，为球迷提供一个**实时、美观、易用**的LeBron James数据展示平台。

### 1.2 项目目标

**核心目标**：
- 展示LeBron James的实时比赛数据和生涯累计数据
- 支持PC端和移动端自适应展示
- 对接NBA官方数据源，确保数据准确
- 采用Lakers紫金配色，致敬传奇

**业务目标**：
| 目标 | 指标 |
|------|------|
| 首屏加载时间 | < 2秒 |
| 数据刷新间隔 | 5分钟（今日战报）|
| 用户覆盖 | PC端 + 移动端 |
| 数据准确率 | 99.9% |

### 1.3 目标用户

- **LeBron James球迷**：追踪每场比赛数据
- **NBA数据爱好者**：了解历史排名
- **篮球博主/自媒体**：生成数据海报

### 1.4 项目范围

**包含功能**：
- 今日战报展示
- 生涯累计统计
- 历史排名对比
- 响应式布局
- 自动数据刷新

**不包含功能**：
- 用户注册登录
- 数据收藏
- 社交分享
- 多语言支持

---

## 2. 功能需求

### 2.1 功能架构图

```
┌─────────────────────────────────────────────────────────┐
│                    LeBron James 数据展示                 │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   今日战报   │  │   生涯累计   │  │   历史排名   │  │
│  │  比赛数据    │  │  常规赛统计  │  │  NBA历史地位 │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ 后端API  │   │ Mock数据 │   │ 前端展示 │
        └──────────┘   └──────────┘   └──────────┘
```

### 2.2 今日战报模块

**功能编号**：F-001  
**功能名称**：今日战报展示  
**优先级**：高  
**描述**：展示LeBron最近一场比赛的详细数据

**展示内容**：

| 字段 | 中文名称 | 数据类型 | 示例值 |
|------|---------|---------|--------|
| opponent | 对手球队 | string | 勇士 |
| date | 比赛日期 | string (YYYY-MM-DD) | 2025-03-28 |
| date_local | 本地日期 | string | 2025年3月28日 |
| timezone | 时区代码 | string | CN |
| result | 比赛结果 | string (W/L) | W |
| points | 得分 | number | 28 |
| rebounds | 篮板 | number | 8 |
| assists | 助攻 | number | 6 |
| steals | 抢断 | number | 2 |
| blocks | 盖帽 | number | 1 |
| minutes | 出场时间 | number | 34 |
| fgPercent | 投篮命中率 | number | 52.4 |
| threePercent | 三分命中率 | number | 40.0 |
| ftPercent | 罚球命中率 | number | 85.7 |

**业务规则**：
- 比赛日：展示当日比赛数据
- 非比赛日：展示最近一场比赛数据
- 休赛期：显示"暂无比赛数据"提示

**PC端展示**：
- 位于页面中部，Card组件包裹
- 左侧显示比赛结果（胜/负）
- 中部显示5项基础数据（得分、篮板、助攻、抢断、盖帽）
- 底部显示3项命中率

**移动端展示**：
- Tab切换中"今日战报"页面
- 紧凑布局，5项数据横向排列
- 命中率使用小型卡片展示

### 2.3 生涯累计模块

**功能编号**：F-002  
**功能名称**：生涯累计统计  
**优先级**：高  
**描述**：展示LeBron常规赛生涯累计数据

**展示内容**：

| 字段 | 中文名称 | 数据类型 | 示例值 |
|------|---------|---------|--------|
| games | 出场次数 | number | 1615 |
| points | 总得分 | number | 43241 |
| rebounds | 总篮板 | number | 11992 |
| assists | 总助攻 | number | 11904 |
| steals | 总抢断 | number | 2319 |
| blocks | 总盖帽 | number | 1147 |
| minutes | 总时间（分钟）| number | 59390 |
| tripleDoubles | 三双次数 | number | 122 |

**数据分类展示**：

**第一行（核心数据）**：
- 出场、得分、篮板、助攻

**第二行（辅助数据）**：
- 抢断、盖帽、时间、三双

**每项数据展示格式**：
```
┌─────────────────┐
│   得分          │
│  43,241         │
├─────────────────┤
│ #1 领先第2名4854 │
└─────────────────┘
```

### 2.4 历史排名模块

**功能编号**：F-003  
**功能名称**：历史排名展示  
**优先级**：高  
**描述**：展示LeBron在NBA历史排行榜中的位置

**排名类别（8项）**：

| 类别 | 当前排名 | 历史地位 | 与上一名差距 |
|------|----------|----------|-------------|
| 总得分 | 第1名 | 历史得分王 | 领先第2名 |
| 总助攻 | 第4名 | 历史前列 | 距第3名差 |
| 总篮板 | 第23名 | 前列水平 | 距第22名差 |
| 总抢断 | 第8名 | 历史前列 | 领先第9名 |
| 总盖帽 | 第78名 | 中等水平 | 距第77名差 |
| 总出场 | 第1名 | 历史出场王 | 领先第2名 |
| 总三双 | 第5名 | 历史前列 | 领先第6名 |
| 总时间 | 第2名 | 即将第一 | 距第1名差 |

**排名展示规则**：

| 排名 | 徽章样式 | 差距显示 |
|------|---------|---------|
| 第1名 | 金色背景 `#FDB927` | "领先第2名 XXXX" |
| 前3名 | 白色背景+金色文字 | "领先第N名 XXXX" 或 "距XXX差 XXXX" |
| 其他 | 半透明白色背景 | "距XXX差 XXXX" |

### 2.5 响应式设计

**功能编号**：F-004  
**功能名称**：响应式布局  
**优先级**：高

**断点设计**：

| 设备 | 断点 | 布局方式 |
|------|------|---------|
| PC端 | ≥ 1024px | 16:10海报式布局 |
| 平板 | 768px - 1023px | 单列布局，保持间距 |
| 移动端 | < 768px | Tab切换布局 |

**PC端布局（PCPoster）**：
```
┌─────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────────────┐  │
│  │              │  │  THE KING            │  │
│  │   LeBron     │  │  LEBRON JAMES        │  │
│  │   图片       │  │                      │  │
│  │              │  │  ┌────────────────┐  │  │
│  │   (2/5宽度)   │  │  │ 今日战报       │  │  │
│  │              │  │  └────────────────┘  │  │
│  │              │  │  ┌────────────────┐  │  │
│  │              │  │  │ 生涯累计       │  │  │
│  │              │  │  └────────────────┘  │  │
│  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────┘
```

**移动端布局（MobilePoster）**：
```
┌─────────────────────┐
│   LeBron图片横幅     │
│   THE KING          │
│   LEBRON JAMES      │
├─────────────────────┤
│ [今日战报][生涯累计] │ ← Tab切换
├─────────────────────┤
│                     │
│   当前Tab内容        │
│                     │
└─────────────────────┘
```

### 2.6 自动刷新机制

**功能编号**：F-005  
**功能名称**：数据自动刷新  
**优先级**：中

**刷新策略**：

| 数据类型 | 刷新间隔 | 缓存时长 | 触发条件 |
|---------|---------|---------|---------|
| 今日战报 | 实时获取 | 1小时 | 每次请求调用API验证 |
| 生涯统计 | 24小时 | 24小时 | 缓存过期时刷新 |
| 历史排名 | 7天 | 7天 | 缓存过期时刷新 |

**业务规则**：
- 仅在使用真实API时自动刷新
- Mock模式下不自动刷新
- 提供手动刷新按钮
- 页面可见性变化时（tab切换回前台）可选择性刷新

---

## 3. 技术架构

### 3.1 整体架构

```
┌────────────────────────────────────────────────────────────┐
│                        技术架构                             │
├────────────────────────────────────────────────────────────┤
│  前端层    │  React 19 + TypeScript + Vite 7               │
│  UI组件    │  Radix UI + Tailwind CSS + shadcn/ui         │
│  图表      │  Recharts                                    │
│  状态管理  │  React Hooks (useState/useEffect)            │
│  API层     │  Fetch API                                   │
├────────────────────────────────────────────────────────────┤
│  后端层    │  FastAPI (Python)                            │
│  数据源    │  NBA Stats API (nba_api库)                   │
│  缓存      │  内存缓存 (5分钟)                            │
└────────────────────────────────────────────────────────────┘
```

### 3.2 前端技术栈

**核心依赖**：

| 依赖 | 版本 | 用途 |
|------|------|------|
| react | ^19.2.0 | UI框架 |
| react-dom | ^19.2.0 | DOM渲染 |
| typescript | ~5.9.3 | 类型系统 |
| vite | ^7.2.4 | 构建工具 |
| tailwindcss | ^3.4.19 | CSS框架 |
| @radix-ui/* | latest | 基础UI组件 |
| recharts | ^2.15.4 | 图表库 |
| lucide-react | ^0.562.0 | 图标库 |

**开发依赖**：
- ESLint 9.x
- TypeScript ESLint
- PostCSS
- Autoprefixer

### 3.3 后端技术栈

**核心依赖**：

| 依赖 | 版本 | 用途 |
|------|------|------|
| fastapi | ^0.109.0 | Web框架 |
| uvicorn | ^0.27.0 | ASGI服务器 |
| nba_api | ^1.11.4 | NBA官方API |
| pandas | ^2.1.4 | 数据处理 |
| python-dotenv | ^1.0.0 | 环境变量 |

### 3.4 项目目录结构

```
lebron-stats-fullstack/
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 api/           # API调用封装
│   │   │   └── statsApi.ts
│   │   ├── 📁 components/    # UI组件
│   │   │   └── 📁 ui/        # 50+ shadcn/ui组件
│   │   ├── 📁 data/          # 数据类型定义
│   │   │   └── stats.ts
│   │   ├── 📁 hooks/         # 自定义Hooks
│   │   │   ├── useStats.ts
│   │   │   ├── useMockStats.ts
│   │   │   └── useUnifiedStats.ts
│   │   ├── 📁 mock/          # Mock数据服务
│   │   │   ├── mockApi.ts
│   │   │   └── mockData.ts
│   │   ├── 📁 pages/         # 页面组件
│   │   │   ├── PCPoster.tsx
│   │   │   └── MobilePoster.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── 📁 public/images/     # 静态资源
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── 📁 backend/
│   ├── main.py               # API入口
│   ├── nba_data_client.py    # NBA数据客户端
│   ├── requirements.txt      # Python依赖
│   ├── 📁 data/              # 数据文件
│   └── .env                  # 环境变量
│
├── 📁 scripts/               # 启动脚本
│   ├── start-all.ps1         # Windows一键启动
│   ├── start-backend.ps1     # Windows启动后端
│   ├── start-frontend.ps1    # Windows启动前端
│   ├── start-all.sh          # Linux/Mac一键启动
│   ├── start-backend.sh
│   └── start-frontend.sh
│
└── README.md
```

### 3.5 数据流架构

```
用户界面(PC/Mobile)
    │
    ▼
useUnifiedStats (统一数据入口)
    │
    ├─ useStats (真实API)
    │     │
    │     ▼
    │  statsApi.ts ──→ Fetch API ──→ 后端服务 ──→ NBA官方API
    │
    └─ useMockStats (Mock数据)
          │
          ▼
       mockApi.ts ──→ mockData.ts (本地Mock数据)
```

---

## 4. 数据规范

### 4.1 数据类型定义

#### 4.1.1 今日战报 (TodayGameStats)

```typescript
interface TodayGameStats {
  /** 对手球队名称 */
  opponent: string;
  /** 比赛日期，格式：YYYY-MM-DD */
  date: string;
  /** 本地日期，根据访问者IP时区显示（如：2025年3月28日） */
  date_local?: string;
  /** 时区代码（如：CN、US-CA） */
  timezone?: string;
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
```

#### 4.1.2 生涯累计 (CareerStats)

```typescript
interface CareerStats {
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
```

#### 4.1.3 历史排名 (RankingData)

```typescript
interface RankingData {
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
```

### 4.2 数据格式化

#### 4.2.1 数字格式化

```typescript
// 千分位分隔
formatNumber(43241) // "43,241"

// 差距显示
formatGap(1, 4854, "贾巴尔")    // "领先第2名 4,854"
formatGap(4, -1569, "纳什")     // "距纳什差 1,569"
formatGap(8, 9, "奇克斯")       // "领先第9名 9"
```

#### 4.2.2 数据验证规则

| 字段 | 验证规则 | 错误处理 |
|------|---------|---------|
| opponent | 非空字符串 | 显示"未知对手" |
| date | 符合YYYY-MM-DD格式 | 显示当前日期 |
| result | W 或 L | 默认显示W |
| points | 0-100 | 显示实际值 |
| percentages | 0-100 | 四舍五入到1位小数 |

---

## 5. 接口规范

### 5.1 接口清单

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 今日战报 | GET | `/api/today-game` | 获取最近一场比赛数据 |
| 生涯统计 | GET | `/api/career-stats` | 获取生涯数据+历史排名 |
| 批量获取 | GET | `/api/all-stats` | 一次性获取所有数据 |
| 健康检查 | GET | `/api/health` | 服务健康状态 |

### 5.2 接口详细定义

#### 5.2.1 获取今日战报

**请求**：
```http
GET /api/today-game
Content-Type: application/json
```

**成功响应 (200)**：
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

**特殊情况 (204)**：
```json
{
  "message": "No game data available"
}
```

#### 5.2.2 获取生涯统计数据

**请求**：
```http
GET /api/career-stats
Content-Type: application/json
```

**成功响应 (200)**：
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

#### 5.2.3 批量获取所有数据

**请求**：
```http
GET /api/all-stats
Content-Type: application/json
```

**成功响应 (200)**：
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
    ]
  }
}
```

#### 5.2.4 健康检查

**请求**：
```http
GET /api/health
```

**响应**：
```json
{
  "status": "healthy",
  "timestamp": "2026-04-01T10:30:00",
  "api_version": "1.0.0"
}
```

### 5.3 错误处理

#### 5.3.1 HTTP状态码

| 状态码 | 场景 | 响应格式 |
|--------|------|----------|
| 200 | 请求成功 | 数据对象 |
| 204 | 无比赛日 | `{ "message": "..." }` |
| 400 | 参数错误 | `{ "error": { "code": "...", "message": "..." } }` |
| 500 | 服务器错误 | `{ "error": { "code": "...", "message": "..." } }` |
| 503 | 数据源不可用 | `{ "error": { "code": "...", "message": "..." } }` |

#### 5.3.2 错误响应格式

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "详细错误描述"
  }
}
```

#### 5.3.3 常见错误码

| 错误码 | 说明 |
|--------|------|
| DATA_NOT_FOUND | 比赛数据不存在 |
| SERVER_ERROR | 服务器内部错误 |
| DATA_SOURCE_UNAVAILABLE | NBA API服务不可用 |
| INTERNAL_SERVER_ERROR | 未知服务器错误 |

---

## 6. UI/UX设计规范

### 6.1 配色方案

**Lakers紫金主题**：

| 用途 | 颜色代码 | 说明 |
|------|---------|------|
| 主色（紫色）| `#552583` | Lakers紫 |
| 辅助色（深紫）| `#311557` | 深紫色 |
| 强调色（金色）| `#FDB927` | Lakers金 |
| 背景色 | `#000000` | 黑色背景 |
| 文字主色 | `#FFFFFF` | 白色文字 |
| 文字次色 | `rgba(255,255,255,0.6)` | 60%白色 |

### 6.2 字体规范

| 元素 | 字体 | 大小 | 字重 |
|------|------|------|------|
| 主标题 | 系统默认 | 48-72px | black (900) |
| 副标题 | 系统默认 | 24-32px | bold (700) |
| 数据大数字 | 系统默认 | 32-48px | black (900) |
| 数据标签 | 系统默认 | 12-14px | normal (400) |
| 正文 | 系统默认 | 14-16px | normal (400) |

### 6.3 组件规范

#### 6.3.1 统计卡片

```
样式：
- 圆角：rounded-xl (12px)
- 背景：bg-gradient-to-b from-white/10 to-white/5
- 边框：border border-white/10
- 内边距：p-4 (16px)
- 悬停：hover:scale-105 transition-transform
```

#### 6.3.2 排名徽章

| 排名 | 背景色 | 文字色 |
|------|--------|--------|
| 第1名 | `#FDB927` (金色) | `#000000` (黑色) |
| 前3名 | `rgba(255,255,255,0.2)` | `#FDB927` (金色) |
| 其他 | `rgba(255,255,255,0.1)` | `rgba(255,255,255,0.7)` |

#### 6.3.3 Tab切换（移动端）

```
样式：
- 背景：bg-white/5
- 选中：bg-[#FDB927] text-black
- 未选中：text-white/70
- 圆角：rounded-xl
```

### 6.4 图片资源

| 资源 | 文件名 | 尺寸 | 用途 |
|------|--------|------|------|
| LeBron主图 | lebron-purple.jpg | 1920x1080 | 主视觉 |
| LeBron备选 | lebron-king.jpg | 1920x1080 | 备选 |

### 6.5 动画效果

| 效果 | 触发条件 | 时长 | 缓动函数 |
|------|---------|------|---------|
| 卡片悬停放大 | hover | 200ms | ease-out |
| 数据加载旋转 | loading | infinite | linear |
| Tab切换 | click | 150ms | ease-in-out |
| 页面进入 | mount | 300ms | ease-out |

---

## 7. 非功能需求

### 7.1 性能要求

| 指标 | 目标值 | 最大值 |
|------|--------|--------|
| 首屏加载时间 | < 1.5s | < 2s |
| API响应时间 | < 200ms | < 500ms |
| 页面交互延迟 | < 50ms | < 100ms |
| 内存占用 | < 100MB | < 150MB |

### 7.2 兼容性要求

| 浏览器 | 版本要求 |
|--------|---------|
| Chrome | ≥ 90 |
| Firefox | ≥ 88 |
| Safari | ≥ 14 |
| Edge | ≥ 90 |

| 设备 | 要求 |
|------|------|
| PC | 支持1920x1080及以上分辨率 |
| 平板 | 支持横竖屏切换 |
| 手机 | 支持主流手机屏幕尺寸 |

### 7.3 可用性要求

- **可用性指标**：99.5%
- **故障恢复时间**：< 5分钟
- **数据备份**：每日自动备份

### 7.4 安全要求

- **CORS配置**：只允许指定域名访问
- **输入验证**：所有API输入参数验证
- **错误信息**：不暴露内部错误详情
- **日志脱敏**：敏感信息不打入日志

---

## 8. 开发规范

### 8.1 代码规范

**TypeScript规范**：
- 严格模式启用 (`strict: true`)
- 禁止隐式any
- 所有函数需标注返回类型
- 使用interface定义对象类型

**命名规范**：
- 组件：PascalCase (e.g., `PCPoster.tsx`)
- hooks：camelCase以use开头 (e.g., `useStats.ts`)
- 工具函数：camelCase (e.g., `formatNumber`)
- 常量：UPPER_SNAKE_CASE

### 8.2 环境配置

**前端环境变量**：
```bash
# .env
VITE_USE_MOCK=false
VITE_API_BASE_URL=http://localhost:3000/api
```

**后端环境变量**：
```bash
# .env
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
LOG_LEVEL=INFO
```

### 8.3 Mock模式

**用途**：
- 前端独立开发
- UI测试
- 演示环境

**切换方式**：
```bash
# 使用Mock数据
VITE_USE_MOCK=true

# 使用真实API
VITE_USE_MOCK=false
```

---

## 9. 部署规范

### 9.1 部署架构

```
用户
  │
  ▼
┌──────────┐
│  Nginx   │ ← 反向代理、静态资源
└────┬─────┘
     │
     ├──────────────┐
     ▼              ▼
┌──────────┐  ┌──────────┐
│ 前端静态  │  │ FastAPI  │
│ 资源     │  │ 后端服务  │
└──────────┘  └──────────┘
                    │
                    ▼
               ┌──────────┐
               │ NBA API  │
               └──────────┘
```

### 9.2 构建输出

**前端构建**：
```
dist/
├── index.html
├── assets/
│   ├── index-xxx.css
│   └── index-xxx.js
└── images/
    └── lebron-purple.jpg
```

### 9.3 部署检查清单

- [ ] 代码构建成功（`npm run build`）
- [ ] TypeScript类型检查通过
- [ ] ESLint无错误
- [ ] 环境变量配置正确
- [ ] API地址可访问
- [ ] CORS配置允许前端域名
- [ ] 静态资源路径正确
- [ ] 健康检查接口正常

### 9.4 推荐部署平台

| 平台 | 适用场景 | 部署方式 |
|------|---------|---------|
| Vercel | 前端 | Git集成自动部署 |
| Netlify | 前端 | Git集成自动部署 |
| Railway/Render | 后端 | Docker/直接部署 |
| 阿里云/腾讯云 | 全栈 | 云服务器手动部署 |

---

## 10. 测试策略

### 10.1 测试类型

| 测试类型 | 工具 | 覆盖率要求 |
|---------|------|-----------|
| 单元测试 | Jest + React Testing Library | ≥ 80% |
| 集成测试 | Cypress | 核心流程100% |
| E2E测试 | Playwright | 主要场景100% |
| 性能测试 | Lighthouse | 性能得分≥90 |

### 10.2 Mock数据测试

**测试场景**：
- ✅ 今日战报数据格式
- ✅ 生涯统计数据格式
- ✅ 历史排名数据格式
- ✅ 空数据场景（无比赛日）
- ✅ 网络延迟模拟
- ✅ 错误处理流程

### 10.3 集成测试场景

**正常流程**：
1. 首次加载显示Loading状态
2. 数据加载成功后渲染
3. 5分钟后自动刷新
4. 手动刷新按钮可用

**异常流程**：
1. 网络超时处理（显示重试按钮）
2. API返回500错误（显示错误信息）
3. 无比赛日（显示空状态）

**响应式测试**：
1. PC端大屏展示（1920x1080）
2. 平板横屏/竖屏（768px-1024px）
3. 手机端展示（< 768px）
4. Tab切换功能正常

### 10.4 性能测试指标

| 指标 | 目标值 | 测试工具 |
|------|--------|---------|
| FCP (首次内容绘制) | < 1s | Lighthouse |
| LCP (最大内容绘制) | < 2s | Lighthouse |
| TTI (可交互时间) | < 3s | Lighthouse |
| CLS (累积布局偏移) | < 0.1 | Lighthouse |

---

## 附录

### A. 参考资料

- [NBA Stats API Documentation](https://github.com/swar/nba_api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [shadcn/ui Documentation](https://ui.shadcn.com/)

### B. 术语表

| 术语 | 说明 |
|------|------|
| CORS | 跨域资源共享 (Cross-Origin Resource Sharing) |
| API | 应用程序接口 (Application Programming Interface) |
| Mock | 模拟数据/接口 |
| SPA | 单页应用 (Single Page Application) |
| SSR | 服务端渲染 (Server-Side Rendering) |
| CSR | 客户端渲染 (Client-Side Rendering) |

### C. 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.1.0 | 2026-04-02 | API优化、智能缓存、时区感知、局域网支持 |
| v1.0.0 | 2026-04-01 | 初始版本，完整功能实现 |

---

*文档结束*
