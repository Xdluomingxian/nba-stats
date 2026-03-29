# LeBron James 数据展示 - 后端交付包

## 📦 交付包说明

此文件夹包含前端项目与后端对接所需的全部文档和参考代码，供后端开发人员快速理解和实现API接口。

---

## 📁 文件夹结构

```
backend-delivery/
├── 📄 .env.example                 # 环境变量配置示例
├── 📁 docs/                        # 项目文档
│   ├── backend-api-requirements.md # 后端API开发需求文档（主要参考）
│   └── API_DOCUMENTATION.md        # API接口文档（如有）
├── 📁 api-contract/                # API契约 - 前后端约定
│   ├── stats.ts                    # 数据类型定义（TypeScript）
│   └── statsApi.ts                 # API调用封装参考
├── 📁 mock-data/                   # Mock数据参考
│   ├── mockApi.ts                  # Mock API实现逻辑
│   └── mockData.ts                 # Mock测试数据
├── 📁 frontend-reference/          # 前端参考代码
│   ├── useStats.ts                 # 前端Hook（展示API调用方式）
│   └── package.json                # 前端项目依赖
└── 📁 scripts/                     # 测试脚本
    └── test-mock.mjs               # Mock API测试脚本
```

---

## 🎯 后端开发人员必读

### 1️⃣ 首先阅读
**`docs/backend-api-requirements.md`** - 完整的API开发需求文档，包含：
- 3个API接口的详细定义
- 请求/响应格式
- 错误处理规范
- 性能要求
- 数据结构定义

### 2️⃣ 数据类型参考
**`api-contract/stats.ts`** - 核心的TypeScript接口定义：
- `TodayGameStats` - 今日战报数据结构
- `CareerStats` - 生涯统计数据结构
- `RankingData` - 历史排名数据结构

### 3️⃣ API调用参考
**`api-contract/statsApi.ts`** - 前端API调用封装，帮助理解：
- API基础URL配置
- 请求路径和参数
- 错误处理方式

### 4️⃣ Mock数据参考
**`mock-data/`** 文件夹包含Mock实现：
- 可直接运行的Mock数据
- 测试数据示例
- 动态数据生成逻辑（如基于日期的微变得分）

---

## 🔌 核心API接口

| 接口 | 路径 | 说明 |
|------|------|------|
| 今日战报 | `GET /api/today-game` | 获取最近一场比赛数据 |
| 生涯统计 | `GET /api/career-stats` | 生涯累计数据 + 历史排名 |
| 批量获取 | `GET /api/all-stats` | 一次性获取所有数据 |

**基础URL**: `http://localhost:3000/api`（开发环境）

---

## 🛠️ 技术建议

### 推荐技术栈
- **Node.js**: Express.js / Fastify / NestJS
- **Python**: FastAPI / Flask / Django
- **缓存**: Redis（可选）
- **数据源**: NBA Stats API / Basketball-Reference

### 性能目标
- 今日战报: < 200ms
- 生涯统计: < 300ms
- 批量获取: < 500ms

### 缓存策略
- 今日战报: 5分钟
- 生涯统计: 1小时
- 历史排名: 24小时

---

## 🧪 测试建议

1. 使用 `mock-data/` 中的数据作为测试基准
2. 运行 `scripts/test-mock.mjs` 了解Mock行为
3. 确保返回格式与 `api-contract/stats.ts` 完全一致

---

## 📞 联系方式

- **前端开发**: [负责React应用开发]
- **后端开发**: [负责API实现]
- **对接问题**: 请参照 `docs/backend-api-requirements.md` 中的规范

---

## 📝 变更记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2025-03-29 | v1.0 | 初始版本交付 |

