# 🏀 NBA 詹姆斯数据展示 - 前端

勒布朗·詹姆斯职业生涯数据展示页面，包含今日战报、生涯统计和历史排名。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/ubuntu/projects/nba-stats/frontend
npm install
```

### 2. 启动开发服务器

```bash
# 确保后端 API 已启动 (http://localhost:3000)
npm run dev
```

访问：http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
npm run preview
```

## 📁 项目结构

```
frontend/
├── src/
│   ├── App.tsx              # 主页面组件
│   ├── index.css            # 全局样式
│   ├── main.tsx             # 入口文件
│   ├── api/
│   │   └── statsApi.ts      # API 调用
│   ├── hooks/
│   │   └── useStats.ts      # 数据获取 Hook
│   └── types/
│       └── stats.ts         # TypeScript 类型定义
├── .env                     # 环境变量
├── tailwind.config.js       # Tailwind 配置
└── package.json             # 依赖配置
```

## 🎨 技术栈

- **框架**: React 19 + TypeScript
- **构建工具**: Vite 7
- **样式**: Tailwind CSS
- **图标**: Lucide React
- **图表**: Recharts (可选)

## 📊 功能特性

- ✅ 今日战报展示（得分、篮板、助攻等）
- ✅ 生涯统计数据（8 项核心数据）
- ✅ 历史排名展示（8 项历史排名）
- ✅ 自动刷新（每 5 分钟）
- ✅ 响应式设计（支持移动端）
- ✅ 深色主题（湖人配色）

## 🔧 配置

### 环境变量

创建 `.env` 文件：

```bash
VITE_API_BASE_URL=http://localhost:3000/api
```

### API 接口

后端 API 地址：http://localhost:3000/api

- `/api/today-game` - 今日战报
- `/api/career-stats` - 生涯统计
- `/api/all-stats` - 批量获取

## 🎯 页面预览

### 今日战报
- 对手球队
- 比赛结果（胜/负）
- 详细数据（得分、篮板、助攻、抢断、盖帽）
- 命中率（投篮、三分、罚球）

### 生涯统计
- 出场次数
- 总得分、篮板、助攻
- 总抢断、盖帽
- 三双次数
- 总出场时间

### 历史排名
- 总得分（历史第 1）🥇
- 总助攻（历史第 4）
- 总篮板（历史第 23）
- 总抢断（历史第 8）
- 总盖帽（历史第 78）
- 总出场（历史第 1）🥇
- 总三双（历史第 5）
- 总时间（历史第 2）

## 🐛 故障排除

### API 连接失败

确保后端服务已启动：

```bash
cd /home/ubuntu/projects/nba-stats/backend-delivery
source venv/bin/activate
python src/main.py
```

### 样式问题

清除缓存并重新安装依赖：

```bash
rm -rf node_modules package-lock.json
npm install
```

## 📝 开发日志

### 2026-03-29
- ✅ 创建 React + TypeScript 项目
- ✅ 实现今日战报组件
- ✅ 实现生涯统计组件
- ✅ 实现历史排名组件
- ✅ 添加 Tailwind CSS 样式
- ✅ 配置 API 调用
- ✅ 添加自动刷新功能

---

**版本**: v1.0.0  
**创建时间**: 2026-03-29  
**作者**: 小海螺 × 老罗
