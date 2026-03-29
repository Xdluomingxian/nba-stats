# 🚀 NBA API 快速参考

**基础 URL**: `http://localhost:3000/api`

---

## 📡 接口速查

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 健康检查 | GET | `/health` | 检查 API 状态 |
| 今日战报 | GET | `/today-game` | 最近比赛数据 |
| 生涯统计 | GET | `/career-stats` | 生涯数据 + 排名 |
| 批量获取 | GET | `/all-stats` | 一次性获取所有 |

---

## 🔧 快速测试

```bash
# 健康检查
curl http://localhost:3000/api/health

# 今日战报
curl http://localhost:3000/api/today-game

# 生涯统计
curl http://localhost:3000/api/career-stats

# 批量获取（推荐）
curl http://localhost:3000/api/all-stats
```

---

## 💻 前端调用

```typescript
// 批量获取（推荐）
const response = await fetch('/api/all-stats');
const data = await response.json();

// 数据结构
data.todayGame      // 今日战报
data.career.stats   // 生涯统计
data.career.rankings // 历史排名
```

---

## 📊 当前数据（2026-03-28）

**今日战报**:
- 对手：篮网
- 结果：胜 (W)
- 数据：14 分 6 板 8 助

**生涯统计**:
- 出场：1,615 场 🥇
- 得分：43,290 分 🥇
- 篮板：12,047 个
- 助攻：11,952 次
- 抢断：2,405 次

---

## 🔗 完整文档

- **项目说明**: `PROJECT_DOCUMENTATION.md`
- **接口文档**: `API_DOCUMENTATION.md`
- **Swagger UI**: http://localhost:3000/docs

---

**版本**: v1.0 | **更新**: 2026-03-29
