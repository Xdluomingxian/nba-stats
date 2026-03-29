# 🏀 NBA 统计数据爬虫

基于 API 的 NBA 比赛数据爬虫，支持球员统计、球队数据、比赛结果等数据采集。

## ✨ 功能特性

- 📊 **球员数据** - 得分、篮板、助攻等详细统计
- 🏆 **球队数据** - 胜率、排名、主客场数据
- 📅 **赛程数据** - 历史比赛、未来赛程
- 📈 **数据分析** - 数据可视化、趋势分析
- 💾 **数据存储** - CSV、JSON、MongoDB、飞书多维表格
- ⏰ **定时任务** - 自动更新最新数据

## 🚀 快速开始

### 1. 安装依赖

```bash
cd nba-stats
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件配置 API 密钥和存储选项
```

### 3. 运行爬虫

```bash
# 获取今日比赛数据
python src/main.py --today

# 获取球员数据
python src/main.py --player "LeBron James"

# 获取球队数据
python src/main.py --team "Lakers"

# 获取赛程数据
python src/main.py --schedule
```

## 📊 数据源

### API 选项

| API | 状态 | 说明 |
|-----|------|------|
| **NBA Official API** | ✅ 免费 | 官方数据，最准确 |
| **BallDontLie API** | ✅ 免费 | 简化版，易使用 |
| **MySportsFeeds** | ⚠️ 付费 | 数据全面 |

### 推荐配置

使用 **BallDontLie API**（免费、无需密钥）：
```bash
NBA_API_PROVIDER=balldontlie
```

## 📁 项目结构

```
nba-stats/
├── src/
│   ├── main.py           # 程序入口
│   ├── nba_client.py     # NBA API 客户端
│   ├── data_processor.py # 数据处理
│   ├── storage.py        # 数据存储
│   └── analyzer.py       # 数据分析
├── data/                 # 数据文件
├── docs/                 # 文档
├── tests/                # 测试
├── .env                  # 环境变量
├── requirements.txt      # 依赖包
└── README.md             # 说明文档
```

## 🎯 使用示例

### 获取今日比赛

```bash
python src/main.py --today
```

输出：
```
📅 2026-03-29 比赛

🏀 Lakers vs Warriors
   比分：112 - 108
   最佳球员：LeBron James (32 分 8 篮板 11 助攻)

🏀 Celtics vs Heat
   比分：98 - 95
   最佳球员：Jayson Tatum (28 分 6 篮板 5 助攻)
```

### 获取球员数据

```bash
python src/main.py --player "LeBron James" --season 2025
```

### 获取球队排名

```bash
python src/main.py --standings
```

## 📊 数据字段

### 球员数据
- `player_name` - 球员姓名
- `team` - 所属球队
- `position` - 位置
- `points` - 得分
- `rebounds` - 篮板
- `assists` - 助攻
- `steals` - 抢断
- `blocks` - 盖帽
- `field_goal_pct` - 投篮命中率
- `three_point_pct` - 三分命中率
- `free_throw_pct` - 罚球命中率

### 球队数据
- `team_name` - 球队名称
- `wins` - 胜场
- `losses` - 负场
- `win_pct` - 胜率
- `conference` - 联盟
- `division` - 赛区
- `home_record` - 主场战绩
- `away_record` - 客场战绩

### 比赛数据
- `game_id` - 比赛 ID
- `date` - 比赛日期
- `home_team` - 主队
- `away_team` - 客队
- `home_score` - 主队得分
- `away_score` - 客队得分
- `status` - 比赛状态

## 💾 数据存储

### 支持格式

| 格式 | 配置 | 说明 |
|------|------|------|
| **CSV** | 默认 | `data/nba_data.csv` |
| **JSON** | `ENABLE_JSON=true` | `data/nba_data.json` |
| **MongoDB** | `ENABLE_MONGODB=true` | 数据库存储 |
| **飞书** | `ENABLE_FEISHU=true` | 多维表格 |

### 飞书集成

配置飞书多维表格：
```bash
ENABLE_FEISHU=true
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_secret
FEISHU_SPREADSHEET_TOKEN=your_token
FEISHU_TABLE_ID=your_table_id
```

## ⏰ 定时任务

### 配置 Crontab

```bash
# 每天早上 8 点获取昨日比赛数据
0 8 * * * cd /home/ubuntu/projects/nba-stats && source venv/bin/activate && python src/main.py --yesterday >> logs/nba.log 2>&1

# 比赛日期间每 2 小时更新
0 */2 * * * cd /home/ubuntu/projects/nba-stats && source venv/bin/activate && python src/main.py --latest >> logs/nba.log 2>&1
```

## 📈 数据分析

### 球员排名

```bash
python src/main.py --rank points --top 10
```

输出 Top 10 得分王：
```
🏆 2025-26 赛季得分榜 Top 10

1. Luka Dončić - 33.5 分
2. Joel Embiid - 32.8 分
3. Giannis Antetokounmpo - 31.2 分
...
```

### 球队分析

```bash
python src/main.py --analyze "Lakers"
```

## 🧪 测试

```bash
cd tests
pytest test_nba_client.py -v
pytest test_data_processor.py -v
```

## 📝 环境变量

详见 `.env.example`：

```bash
# API 配置
NBA_API_PROVIDER=balldontlie
NBA_API_KEY=

# 存储配置
ENABLE_MONGODB=false
MONGO_URI=mongodb://127.0.0.1:27017/
DB_NAME=nba_stats

# 飞书配置
ENABLE_FEISHU=false
FEISHU_APP_ID=
FEISHU_APP_SECRET=

# 爬取配置
SEASON=2025
MAX_PAGES=10

# 日志配置
LOG_LEVEL=INFO
```

## 🐛 常见问题

### Q: API 请求失败？

**A**: 检查网络连接，或更换 API 提供商。

### Q: 数据不完整？

**A**: 增加 `MAX_PAGES` 配置，或检查 API 限制。

### Q: 飞书同步失败？

**A**: 检查飞书配置和表格权限。

## 📚 相关资源

- **NBA 官网**: https://www.nba.com
- **BallDontLie API**: https://www.balldontlie.io
- **Basketball Reference**: https://www.basketball-reference.com

## 📄 许可证

MIT License

---

**版本**: v1.0.0  
**创建时间**: 2026-03-29  
**作者**: 小海螺 × 老罗
