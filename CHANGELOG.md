# 更新日志 (Changelog)

## [v1.3.0] - 2026-05-07

### 代码清理

#### 删除死代码文件
- 删除 `backend/nba_data_client_legacy.py`（17KB 旧版客户端，无任何引用）
- 删除 `frontend/src/hooks/useUnifiedStats.ts`（仅 re-export `useStats`）
- 删除 `frontend/src/hooks/useMockStats.ts`（无任何组件引用）
- 删除 `frontend/src/App.css`（未被任何文件 import）
- 删除 `backend/test_fix.py`（临时测试文件）
- 删除 `frontend/public/images/lebron-king.jpg`（未被引用）
- 删除 `backend/package-lock.json`（Python 项目中的 npm 锁文件）
- 删除 `frontend/src/api/statsApi.ts`（未被任何模块引用）

#### 删除未使用的依赖
- 前端移除 26 个未使用的 npm 包：`recharts`、`date-fns`、`zod`、`react-hook-form`、`cmdk`、`sonner`、`kimi-plugin-inspect-react` 等
- 删除 51 个未使用的 shadcn/ui 组件文件，仅保留 `card` 和 `tabs`
- 前端 `package.json` 依赖从 30+ 精简至 6 个

### 架构优化

#### 共享组件抽取
- 新增 `frontend/src/components/stats/` 目录：
  - `StatItem.tsx` — 统计项组件（支持 PC/移动端尺寸切换）
  - `CareerStatWithRank.tsx` — 生涯数据+排名组合组件
  - `StateComponents.tsx` — LoadingState 和 ErrorState 统一封装
- 消除 `PCPoster.tsx` 和 `MobilePoster.tsx` 中 4 组重复组件定义

### API 优化

#### 前端
- `useStats` hook 从 3 次独立 API 请求改为单次调用 `/api/all-stats`
- 减少网络往返，提升首屏加载性能

#### 后端
- `/api/all-stats` 新增 `season_type` 查询参数支持
- 响应中新增 `playoffCareer` 字段，返回季后赛生涯数据

### Bug修复

#### 缓存逻辑修复
- **问题**：`saveLocalCache` 函数已定义但从未被调用，localStorage 缓存从未写入
- **修复**：在 `useStats` 的 `fetchData` 成功后正确调用 `saveLocalCache`
- **增强**：缓存数据结构新增 `playoffCareerStats` 字段

#### Vite 端口冲突
- **问题**：Windows Hyper-V 保留端口范围 5095-5194，导致 Vite 默认端口 5173 启动失败（`EACCES: permission denied`）
- **修复**：端口从 5173 改为 3001，host 从 `0.0.0.0` 改为 `127.0.0.1`

### 后端清理
- 移除 `nba_data_client.py` 中未使用的 `RealTimeDataChecker` 实例化和 `data_validator` 导入
- `data_validator.py` 中的 `RealTimeDataChecker` 类定义保留，后续如需可重新接入

### 文件变更

#### 新增文件
- `frontend/src/components/stats/CareerStatWithRank.tsx`
- `frontend/src/components/stats/StatItem.tsx`
- `frontend/src/components/stats/StateComponents.tsx`
- `frontend/src/components/stats/index.ts`

#### 删除文件
- `backend/nba_data_client_legacy.py`
- `backend/test_fix.py`
- `backend/package-lock.json`
- `frontend/src/App.css`
- `frontend/src/api/statsApi.ts`
- `frontend/public/images/lebron-king.jpg`
- `frontend/src/hooks/useUnifiedStats.ts`
- `frontend/src/hooks/useMockStats.ts`
- `frontend/src/components/ui/accordion.tsx` 等 51 个未使用的 UI 组件

#### 修改文件
- `frontend/package.json` — 精简依赖
- `frontend/vite.config.ts` — 端口、chunk 配置
- `frontend/src/hooks/useStats.ts` — 批量接口、缓存修复
- `frontend/src/pages/PCPoster.tsx` — 使用共享组件
- `frontend/src/pages/MobilePoster.tsx` — 使用共享组件
- `backend/main.py` — `/api/all-stats` 增强
- `backend/nba_data_client.py` — 移除未使用的 `RealTimeDataChecker`

---

## [v1.2.0] - 2026-04-27

### 新增功能

#### 季后赛数据支持
- 新增 `/api/playoff-career-stats` API 接口
- 支持查询 LeBron James 季后赛生涯累计数据
- 后端使用 `playercareerstats.PlayerCareerStats` + `season_totals_post_season` 获取数据

#### 赛季类型切换
- 首页新增常规赛/季后赛 Tab 切换组件
- PC端和移动端均支持赛季类型切换
- 根据选择的赛季类型动态展示对应数据
- 无比赛时显示友好提示（"休赛期暂无比赛"/"季后赛暂无比赛"）

### Bug修复

#### 前端页面空白问题
- **根因**：`lucide-react` 库中不存在 `Basketball` 图标，导致模块导入失败
- **修复**：将 `Basketball` 替换为 `CircleDot` 图标
- **影响文件**：`PCPoster.tsx`、`MobilePoster.tsx`

#### 数据请求级联失败
- **问题**：`Promise.all` 导致单个 API 失败时所有数据丢失
- **修复**：改为独立 try/catch 请求，互不影响
- **影响文件**：`useStats.ts`

#### Windows 编码问题
- 修复 `.env` 文件 GBK 解码错误（移除中文注释）
- 修复日志中 emoji 字符无法编码问题

#### slowapi 限流问题
- 修复 `health_check()` 和 `get_playoff_career_stats()` 缺少 `request: Request` 参数

### 优化改进

#### 赛季计算优化
- 修正赛季计算逻辑：月份 >= 10 使用当前年，月份 < 10 使用上一年
- 修复日期解析问题：使用 `pd.to_datetime(format='mixed')` 正确解析日期
- 修复日期排序：按实际日期排序而非字符串排序

#### 数据真实性
- 移除 `_get_mock_recent_game()` 模拟数据回退
- API 无数据时返回 None，前端显示友好提示
- 确保展示的所有数据均来自 NBA 官方 API

#### 缓存优化
- 比赛数据按赛季类型独立缓存（`recent_game_regular_season` / `recent_game_playoffs`）
- 前端 localStorage 缓存有效期从 5 分钟缩短至 1 分钟

#### 错误处理
- 新增 `ErrorBoundary` 组件捕获渲染错误
- API 请求使用 `safeFetch` 封装，失败时返回 null 而非抛出异常

### 代码质量
- 添加 `.gitignore` 配置文件
- 修复 Git 合并冲突标记残留问题

### 文件变更

#### 新增文件
- `frontend/src/components/ErrorBoundary.tsx` - 错误边界组件
- `.gitignore` - Git 忽略规则配置

#### 修改文件
- `backend/nba_data_client.py` - 新增季后赛数据获取、赛季类型支持
- `backend/main.py` - 新增 `/api/playoff-career-stats` 端点、修复 slowapi 参数
- `frontend/src/hooks/useStats.ts` - 赛季类型状态管理、独立 API 请求
- `frontend/src/api/statsApi.ts` - 新增 `fetchPlayoffCareerStats`、赛季类型参数
- `frontend/src/pages/PCPoster.tsx` - 赛季类型切换、条件渲染
- `frontend/src/pages/MobilePoster.tsx` - 赛季类型切换、条件渲染

---

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

### [v1.3.0] - 计划中
- [ ] 完整湖人赛程数据导入
- [ ] 比赛实时状态检测
- [ ] 更多球员数据支持
- [ ] 数据导出功能

### [v2.0.0] - 未来规划
- [ ] 多球员对比功能
- [ ] 历史赛季数据查询
- [ ] 用户自定义主题
- [ ] 社交分享功能
- [ ] 微信小程序版本