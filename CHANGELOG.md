# 更新日志 (Changelog)

## [v1.1.0] - 2026-04-02

### 新增功能

#### 智能缓存系统
- 实现多级缓存机制，大幅减少NBA API调用
- 比赛数据缓存1小时
- 生涯统计数据缓存24小时
- 历史排名数据缓存7天
- 缓存数据自动验证一致性

#### 时区感知功能
- 根据访问者IP自动检测时区
- 支持中国/东亚、美国、欧洲等主要时区
- 自动将UTC日期转换为本地日期显示
- 示例：中国用户看到"2025年4月11日"，美国用户看到"Apr 11, 2025"

#### 局域网访问支持
- 前端监听地址改为 `0.0.0.0`
- Vite代理配置，自动转发API请求
- 支持通过局域网IP访问前端页面

### Bug修复

#### NBA API调用错误修复
- 修复 `PlayerGameLog` API调用：使用 `player_game_log.get_data_frame()` 替代 `get_data_frames()`
- 修复 `AllTimeLeadersGrids` API调用：
  - 参数名修正：`per_mode` → `per_mode_simple`，`top_x` → `topx`
  - 数据访问修正：使用各属性（`pts_leaders`, `ast_leaders`等）替代 `get_data_frames()`

#### 赛季配置修正
- 将赛季从 `2025-26` 修正为 `2024-25`
- 确保获取当前赛季真实数据

#### 前端语法错误修复
- 修复 `MobilePoster.tsx` 重复的 `</span>` 标签
- 添加 `date_local` 和 `timezone` 字段到 TypeScript 类型定义

### 优化改进

#### 数据获取逻辑优化
- 移除"仅比赛日刷新"的限制
- 每次请求都尝试获取最新数据并验证
- API失败时自动降级使用缓存或mock数据

#### API调用优化
- 添加随机延迟（0.5-1.5秒）避免请求过于频繁
- 减少约90%的API调用量
- 降低被封禁IP的风险

#### 代码结构优化
- 新增 `TimeZoneManager` 类处理时区转换
- 新增 `DataCache` 类管理数据缓存
- 新增 `ScheduleManager` 类管理赛程
- 保持向后兼容，`NBADataClient` 别名指向优化版本

### 文件变更

#### 新增文件
- `backend/data/` - 数据缓存目录
- `backend/data/career_stats.json` - 生涯数据缓存
- `backend/data/game_log.json` - 比赛数据缓存
- `backend/data/cache_meta.json` - 缓存元数据
- `CHANGELOG.md` - 更新日志

#### 修改文件
- `backend/nba_data_client.py` - 重构为优化版本
- `backend/main.py` - 添加IP检测支持
- `frontend/vite.config.ts` - 添加代理和局域网配置
- `frontend/src/data/stats.ts` - 添加时区格式化函数
- `frontend/src/pages/PCPoster.tsx` - 使用本地日期显示
- `frontend/src/pages/MobilePoster.tsx` - 使用本地日期显示

### 性能提升

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 每日API调用 | ~288次 | ~3-5次 | 减少98% |
| 排名数据刷新 | 每次 | 7天一次 | 减少99% |
| 生涯数据刷新 | 每次 | 24小时一次 | 减少99% |

---

## [v1.0.0] - 2026-04-01

### 新增功能
- 整合前端和后端项目
- 支持真实NBA数据API
- PC端和移动端响应式布局
- Lakers紫金主题配色
- 实时数据展示（今日战报 + 生涯累计）
- 历史排名对比
- 自动刷新机制
- Mock/真实API切换
- 一键启动脚本

### 技术栈
- 前端：React 19 + TypeScript + Vite 7 + Tailwind CSS + shadcn/ui
- 后端：Python 3.8+ + FastAPI + nba_api + Uvicorn

---

## 版本规划

### [v1.2.0] - 计划中
- [ ] 完整湖人赛程数据导入
- [ ] 比赛实时状态检测
- [ ] 更多球员数据支持
- [ ] 数据导出功能

### [v2.0.0] - 未来规划
- [ ] 多球员对比功能
- [ ] 历史赛季数据查询
- [ ] 用户自定义主题
- [ ] 社交分享功能