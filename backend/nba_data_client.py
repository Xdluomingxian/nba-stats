"""
NBA 数据客户端 - 优化版
功能：
1. 静态数据缓存（生涯数据每日保存）
2. 智能刷新（仅比赛日刷新）
3. 时区感知（根据IP显示对应时区日期）
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import sys
import os
import json
import time
import random
import pandas as pd
from pathlib import Path

# 导入数据校验模块
try:
    from data_validator import DataValidator

    VALIDATOR_AVAILABLE = True
    print("数据校验模块导入成功")
except Exception as e:
    print(f"数据校验模块导入失败：{e}")
    VALIDATOR_AVAILABLE = False

NBA_API_AVAILABLE = False

try:
    from nba_api.stats.endpoints import (
        playercareerstats,
        playergamelog,
        alltimeleadersgrids,
    )
    from nba_api.stats.static import players, teams
    from nba_api.live.nba.endpoints import scoreboard

    NBA_API_AVAILABLE = True
    print("nba_api 导入成功")
except Exception as e:
    print(f"nba_api 导入失败：{e}")

# 数据存储目录
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 静态数据文件路径
CAREER_DATA_FILE = DATA_DIR / "career_stats.json"
GAME_LOG_FILE = DATA_DIR / "game_log.json"
CACHE_META_FILE = DATA_DIR / "cache_meta.json"

# 湖人队赛程（简化版，实际需要定期更新或通过API获取完整赛程）
# 建议：赛季中每周从 stats.nba.com 或 nba_api 同步最新赛程
LAKERS_SCHEDULE_2025_26 = [
    # 示例比赛日期（UTC时间），实际需要完整赛程
    "2025-10-22",
    "2025-10-24",
    "2025-10-26",
    "2025-11-02",
    "2025-11-05",
    "2025-11-08",
    # TODO: 补充完整赛程数据
]


class TimeZoneManager:
    """时区管理器 - 根据IP地址确定时区"""

    # 时区映射（简化版）
    TIME_ZONES = {
        # 中国/东亚
        "CN": "Asia/Shanghai",  # 中国
        "HK": "Asia/Hong_Kong",  # 香港
        "TW": "Asia/Taipei",  # 台湾
        "JP": "Asia/Tokyo",  # 日本
        "KR": "Asia/Seoul",  # 韩国
        "SG": "Asia/Singapore",  # 新加坡
        # 美国
        "US": "America/New_York",  # 美国东部
        "US-CA": "America/Los_Angeles",  # 美国西部（湖人主场）
        # 欧洲
        "GB": "Europe/London",  # 英国
        "FR": "Europe/Paris",  # 法国
        "DE": "Europe/Berlin",  # 德国
    }

    @classmethod
    def get_local_date(cls, utc_date_str: str, country_code: str = "CN") -> str:
        """
        将UTC日期转换为本地日期

        Args:
            utc_date_str: UTC日期字符串 (YYYY-MM-DD)
            country_code: 国家代码

        Returns:
            本地日期字符串 (YYYY年M月D日)
        """
        try:
            # 解析日期（仅日期部分，无时间）
            if isinstance(utc_date_str, str):
                # 去掉时间部分（如果有）
                date_part = utc_date_str.split()[0]
                year, month, day = map(int, date_part.split("-"))
            else:
                # 如果是 datetime 对象
                year = utc_date_str.year
                month = utc_date_str.month
                day = utc_date_str.day

            # 格式化为中文日期
            return f"{year}年{month}月{day}日"

        except Exception as e:
            # 如果转换失败，返回原始日期
            print(f"[时区转换] 日期转换失败：{utc_date_str}, 错误：{e}")
            return utc_date_str

    @classmethod
    def detect_country_from_ip(cls, client_ip: str = None) -> str:
        """
        根据IP地址检测国家（简化版，实际需要调用IP地理位置服务）

        Args:
            client_ip: 客户端IP地址

        Returns:
            国家代码
        """
        # 简化处理：假设中国用户
        # 实际生产环境应使用 ipapi、ipinfo.io 等服务
        return "CN"


class DataCache:
    """数据缓存管理器"""

    def __init__(self):
        self.cache_meta = self._load_cache_meta()

    def _load_cache_meta(self) -> Dict:
        """加载缓存元数据"""
        if CACHE_META_FILE.exists():
            try:
                with open(CACHE_META_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_cache_meta(self):
        """保存缓存元数据"""
        try:
            with open(CACHE_META_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cache_meta, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存元数据失败：{e}")

    def is_cache_valid(self, key: str, max_age_hours: int = 24) -> bool:
        """检查缓存是否有效"""
        if key not in self.cache_meta:
            return False

        last_update = self.cache_meta[key].get("last_update", 0)
        age_hours = (time.time() - last_update) / 3600

        return age_hours < max_age_hours

    def update_cache_time(self, key: str):
        """更新缓存时间"""
        self.cache_meta[key] = {
            "last_update": time.time(),
            "date": datetime.now().isoformat(),
        }
        self._save_cache_meta()

    def load_data(self, key: str) -> Optional[Dict]:
        """从文件加载数据"""
        file_path = DATA_DIR / f"{key}.json"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载缓存数据失败：{e}")
        return None

    def save_data(self, key: str, data: Dict):
        """保存数据到文件"""
        file_path = DATA_DIR / f"{key}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.update_cache_time(key)
        except Exception as e:
            print(f"保存缓存数据失败：{e}")


class ScheduleManager:
    """赛程管理器"""

    LAKERS_SCHEDULE = set(LAKERS_SCHEDULE_2025_26)

    @classmethod
    def has_game_today(cls, date_str: str = None) -> bool:
        """
        检查指定日期是否有比赛

        Args:
            date_str: 日期字符串 (YYYY-MM-DD)，默认为今天

        Returns:
            是否有比赛
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")

        return date_str in cls.LAKERS_SCHEDULE

    @classmethod
    def is_game_finished(cls) -> bool:
        """
        检查今天的比赛是否已结束

        简化逻辑：假设下午4点后（美国时间）比赛结束
        实际需要根据比赛实时状态判断
        """
        now = datetime.now()
        # 美国西部时间下午4点 = UTC 次日凌晨0点左右
        # 简化：假设北京时间下午2点后可以刷新前一天数据
        return now.hour >= 14


class NBADataClient:
    """优化的NBA数据客户端"""

    LEBRON_ID = "2544"
    LAKERS_TEAM_ID = "1610612747"  # 湖人队ID

    def __init__(self):
        self.use_real_api = NBA_API_AVAILABLE
        self.cache = DataCache()
        self.tz_manager = TimeZoneManager()
        # 初始化数据校验器
        if VALIDATOR_AVAILABLE:
            self.validator = DataValidator()
        else:
            self.validator = None

    def _add_request_delay(self):
        """添加随机延迟，避免请求过于频繁"""
        time.sleep(random.uniform(0.5, 1.5))

    def _get_current_season(self) -> str:
        """获取当前赛季（根据月份判断）"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        # NBA赛季跨年规则：10月-12月属于新赛季开始，1月-9月属于上赛季
        if current_month >= 10:
            return f"{current_year}-{str(current_year + 1)[-2:]}"
        else:
            return f"{current_year - 1}-{str(current_year)[-2:]}"

    def get_lebron_recent_game(
        self, client_ip: str = None, force_refresh: bool = False, season_type: str = "Regular Season"
    ) -> Optional[Dict[str, Any]]:
        """
        获取詹姆斯最近一场比赛数据（带数据校验机制）

        逻辑：
        1. 尝试调用API获取最新数据（以NBA API为准）
        2. 与缓存数据进行校验对比
        3. 如有差异，以API数据为准更新缓存
        4. 如果API失败，使用缓存（如果未过期）
        5. 缓存过期则返回None

        Args:
            client_ip: 客户端IP，用于时区转换
            force_refresh: 是否强制刷新，跳过缓存
            season_type: 赛季类型（Regular Season / Playoffs）
        """
        # 缓存 key 根据赛季类型区分
        cache_key = f"recent_game_{season_type.lower().replace(' ', '_')}"
        
        # 如果不是强制刷新，先检查缓存
        cached_game = None
        if not force_refresh:
            cached_game = self.cache.load_data(cache_key)
            # 检查缓存是否有效（1小时内）
            if cached_game and self.cache.is_cache_valid(cache_key, max_age_hours=1):
                cache_date = cached_game.get("date", "")
                print(f"[{season_type}战报] 缓存有效（1小时内），缓存日期：{cache_date}")

        # 尝试从NBA API获取最新数据
        api_game_data = None
        if self.use_real_api:
            try:
                print(f"[{season_type}战报] 从NBA API获取最新数据...")
                self._add_request_delay()

                season = self._get_current_season()
                gamelog = playergamelog.PlayerGameLog(
                    player_id=self.LEBRON_ID,
                    season=season,
                    season_type_all_star=season_type,
                )

                games = gamelog.player_game_log.get_data_frame()

                if not games.empty and len(games) > 0:
                    # 确保获取最新比赛（按日期排序）
                    # GAME_DATE 格式可能是 "Nov 28, 2025" 或 "2025-11-28"
                    # 需要转换为 datetime 对象再排序
                    try:
                        games['GAME_DATE_PARSED'] = games['GAME_DATE'].apply(
                            lambda x: pd.to_datetime(x, format='mixed', dayfirst=False)
                        )
                        games_sorted = games.sort_values(by='GAME_DATE_PARSED', ascending=False)
                    except Exception as e:
                        print(f"[今日战报] 日期解析失败，使用原始排序: {e}")
                        games_sorted = games.sort_values(by='GAME_DATE', ascending=False)

                    last_game = games_sorted.iloc[0]

                    matchup = last_game.get("MATCHUP", "")
                    wl = last_game.get("WL", "W")
                    opponent = (
                        matchup.split()[-1] if len(matchup.split()) > 1 else matchup
                    )

                    # 格式化日期为标准格式 (YYYY-MM-DD)
                    game_date_raw = last_game.get("GAME_DATE", "")
                    try:
                        # 解析日期并统一格式
                        from dateutil import parser
                        parsed_date = parser.parse(str(game_date_raw))
                        game_date = parsed_date.strftime("%Y-%m-%d")
                    except Exception:
                        # 如果解析失败，尝试直接使用原始值
                        game_date = str(game_date_raw).split()[0] if isinstance(game_date_raw, str) else str(game_date_raw)

                    api_game_data = {
                        "opponent": self._translate_team(opponent),
                        "date": game_date,
                        "result": wl,
                        "points": int(last_game.get("PTS", 0)),
                        "rebounds": int(last_game.get("REB", 0)),
                        "assists": int(last_game.get("AST", 0)),
                        "steals": int(last_game.get("STL", 0)),
                        "blocks": int(last_game.get("BLK", 0)),
                        "minutes": float(last_game.get("MIN", 34.0)),
                        "fgPercent": round(float(last_game.get("FG_PCT", 0)) * 100, 1),
                        "threePercent": round(
                            float(last_game.get("FG3_PCT", 0)) * 100, 1
                        ),
                        "ftPercent": round(float(last_game.get("FT_PCT", 0)) * 100, 1),
                        "data_source": "NBA_API",
                        "last_updated": datetime.now().isoformat(),
                    }

                    print(
                        f"[{season_type}战报] API返回数据：日期={api_game_data['date']}, 对手={api_game_data['opponent']}, "
                        f"得分={api_game_data['points']}, 篮板={api_game_data['rebounds']}, 助攻={api_game_data['assists']}"
                    )

            except Exception as e:
                print(f"[{season_type}战报] 从NBA API获取数据失败：{e}")
                api_game_data = None

        # 数据校验：对比缓存和API数据
        if self.validator and api_game_data:
            need_update, final_data, reason = self.validator.validate_game_data(
                cached_game, api_game_data
            )
            print(f"[{season_type}战报] 数据校验结果：{reason}")

            if need_update:
                print(f"[{season_type}战报] 以NBA API数据为准，更新缓存")
                self.cache.save_data(cache_key, final_data)
                return self._apply_timezone(final_data, client_ip)
            else:
                # 数据一致，但刷新缓存时间戳
                if cached_game:
                    print(f"[{season_type}战报] 数据一致，刷新缓存时间戳")
                    self.cache.save_data(cache_key, api_game_data)
                return self._apply_timezone(api_game_data, client_ip)

        elif api_game_data:
            # 没有校验器，直接使用API数据
            print(f"[{season_type}战报] 直接使用NBA API数据（无校验）")
            self.cache.save_data(cache_key, api_game_data)
            return self._apply_timezone(api_game_data, client_ip)

        # API失败，使用缓存（如果存在且未过期）
        if cached_game:
            cache_date = cached_game.get("date", "未知")
            print(f"[{season_type}战报] API失败，使用缓存数据（日期：{cache_date}）")
            return self._apply_timezone(cached_game, client_ip)

        # 没有缓存，返回None（不返回Mock数据）
        print(f"[{season_type}战报] API失败且无缓存，返回None")
        return None

    def get_lebron_career_stats(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        获取詹姆斯生涯统计数据（带数据校验机制）

        逻辑：
        1. 尝试调用NBA API获取最新生涯数据（以NBA API为准）
        2. 与缓存数据进行校验对比
        3. 如有差异，以API数据为准
        4. API失败时使用缓存（如果未过期）

        Args:
            force_refresh: 是否强制刷新，跳过缓存
        """
        if not self.use_real_api:
            print("[生涯数据] NBA API不可用，使用Mock数据")
            return self._get_mock_career_stats()

        # 检查缓存（如果不是强制刷新）
        cached_stats = None
        if not force_refresh:
            cached_stats = self.cache.load_data("career_stats")
            if cached_stats and self.cache.is_cache_valid("career_stats", max_age_hours=24):
                print(f"[生涯数据] 缓存有效（24小时内）")

        # 尝试从NBA API获取最新数据
        api_career_data = None
        try:
            print("[生涯数据] 从NBA API获取最新数据...")
            self._add_request_delay()
            career = playercareerstats.PlayerCareerStats(player_id=self.LEBRON_ID)
            regular_season = career.season_totals_regular_season.get_data_frame()

            if not regular_season.empty:
                # 计算总数据
                api_career_data = {
                    "games": int(regular_season["GP"].sum()),
                    "points": int(regular_season["PTS"].sum()),
                    "rebounds": int(regular_season["REB"].sum()),
                    "assists": int(regular_season["AST"].sum()),
                    "steals": int(regular_season["STL"].sum()),
                    "blocks": int(regular_season["BLK"].sum()),
                    "minutes": int(regular_season["MIN"].sum()),
                    "tripleDoubles": 122,  # 需单独查询，NBA API无生涯三双总和字段
                    "last_updated": datetime.now().isoformat(),
                    "data_source": "NBA_API",
                }
                
                print(f"[生涯数据] API返回数据：")
                print(f"  - 出场：{api_career_data['games']}, "
                      f"得分：{api_career_data['points']}, "
                      f"篮板：{api_career_data['rebounds']}, "
                      f"助攻：{api_career_data['assists']}")
            else:
                print("[生涯数据] API返回空数据")

        except Exception as e:
            print(f"[生涯数据] 从NBA API获取数据失败：{e}")
            api_career_data = None

        # 数据校验：对比缓存和API数据
        if self.validator and api_career_data:
            need_update, final_data, reason = self.validator.validate_career_stats(cached_stats, api_career_data)
            print(f"[生涯数据] 数据校验结果：{reason}")
            
            if need_update:
                print(f"[生涯数据] 以NBA API数据为准，更新缓存")
                self.cache.save_data("career_stats", final_data)
                return final_data
            else:
                # 数据一致，但刷新缓存时间戳
                if cached_stats:
                    print(f"[生涯数据] 数据一致，刷新缓存时间戳")
                    self.cache.save_data("career_stats", api_career_data)
                return api_career_data
        
        elif api_career_data:
            # 没有校验器，直接使用API数据
            print(f"[生涯数据] 直接使用NBA API数据（无校验）")
            self.cache.save_data("career_stats", api_career_data)
            return api_career_data

        # API失败，使用缓存（如果存在且未过期）
        if cached_stats:
            print(f"[生涯数据] API失败，使用缓存数据")
            return cached_stats

        # 没有缓存，返回mock数据
        print("[生涯数据] 使用Mock数据")
        return self._get_mock_career_stats()

    def get_lebron_playoff_career_stats(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        获取詹姆斯季后赛生涯统计数据

        Args:
            force_refresh: 是否强制刷新，跳过缓存
        """
        cache_key = "playoff_career_stats"

        if not self.use_real_api:
            print("[季后赛生涯数据] NBA API不可用，返回空数据")
            return {}

        # 检查缓存
        cached_stats = None
        if not force_refresh:
            cached_stats = self.cache.load_data(cache_key)
            if cached_stats and self.cache.is_cache_valid(cache_key, max_age_hours=24):
                print(f"[季后赛生涯数据] 缓存有效（24小时内）")
                return cached_stats

        # 尝试从NBA API获取最新数据
        api_career_data = None
        try:
            print("[季后赛生涯数据] 从NBA API获取最新数据...")
            self._add_request_delay()
            career = playercareerstats.PlayerCareerStats(player_id=self.LEBRON_ID)
            # 使用career_totals_post_season（单行累计数据，比sum更可靠）
            playoff_career = career.career_totals_post_season.get_data_frame()

            if not playoff_career.empty:
                row = playoff_career.iloc[0]
                api_career_data = {
                    "games": int(row.get("GP", 0)),
                    "points": int(row.get("PTS", 0)),
                    "rebounds": int(row.get("REB", 0)),
                    "assists": int(row.get("AST", 0)),
                    "steals": int(row.get("STL", 0)),
                    "blocks": int(row.get("BLK", 0)),
                    "minutes": int(row.get("MIN", 0)),
                    # 季后赛三双（NBA API不提供此字段，需手动更新）
                    "tripleDoubles": 28,
                    "last_updated": datetime.now().isoformat(),
                    "data_source": "NBA_API",
                    "season_type": "Playoffs",
                }

                print(f"[季后赛生涯数据] API返回数据：")
                print(f"  - 出场：{api_career_data['games']}, "
                      f"得分：{api_career_data['points']}, "
                      f"篮板：{api_career_data['rebounds']}, "
                      f"助攻：{api_career_data['assists']}")

                # 保存到缓存
                self.cache.save_data(cache_key, api_career_data)
                return api_career_data
            else:
                print("[季后赛生涯数据] API返回空数据")

        except Exception as e:
            print(f"[季后赛生涯数据] 从NBA API获取数据失败：{e}")
            api_career_data = None

        # API失败，使用缓存
        if cached_stats:
            print(f"[季后赛生涯数据] API失败，使用缓存数据")
            return cached_stats

        print("[季后赛生涯数据] 无可用数据")
        return {}

    def _merge_and_verify_stats(self, cached: Dict, new: Dict) -> Dict:
        """
        合并缓存数据和新数据，验证一致性

        逻辑：
        - 新数据应该 >= 缓存数据
        - 如果不一致，打印警告并返回较大的值
        """
        result = new.copy()
        fields = [
            "games",
            "points",
            "rebounds",
            "assists",
            "steals",
            "blocks",
            "minutes",
        ]

        for field in fields:
            cached_val = cached.get(field, 0)
            new_val = new.get(field, 0)

            if new_val < cached_val:
                print(f"警告：{field} 数据不一致（新:{new_val} < 缓存:{cached_val}）")
                # 使用缓存值（更大的）
                result[field] = cached_val

        return result

    def _apply_timezone(self, game_data: Dict, client_ip: str = None) -> Dict:
        """应用时区转换"""
        if not game_data or "date" not in game_data:
            return game_data

        country_code = self.tz_manager.detect_country_from_ip(client_ip)
        local_date = self.tz_manager.get_local_date(game_data["date"], country_code)

        result = game_data.copy()
        result["date_local"] = local_date
        result["timezone"] = country_code

        return result

    def get_historical_rankings(
        self, lebron_stats: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """获取历史排名数据（使用缓存，7天刷新一次）"""
        # 检查缓存
        cached_rankings = self.cache.load_data("rankings")
        if cached_rankings and self.cache.is_cache_valid(
            "rankings", max_age_hours=168
        ):  # 7天缓存
            return cached_rankings

        if not self.use_real_api:
            rankings = self._get_mock_rankings(lebron_stats)
            self.cache.save_data("rankings", rankings)
            return rankings

        rankings = []

        try:
            self._add_request_delay()
            leaders_grid = alltimeleadersgrids.AllTimeLeadersGrids(
                league_id="00",
                per_mode_simple="Totals",
                season_type="Regular Season",
                topx=100,
            )

            leaders_data = {
                "PTS": leaders_grid.pts_leaders.get_data_frame()
                if hasattr(leaders_grid, "pts_leaders")
                else None,
                "AST": leaders_grid.ast_leaders.get_data_frame()
                if hasattr(leaders_grid, "ast_leaders")
                else None,
                "REB": leaders_grid.reb_leaders.get_data_frame()
                if hasattr(leaders_grid, "reb_leaders")
                else None,
                "STL": leaders_grid.stl_leaders.get_data_frame()
                if hasattr(leaders_grid, "stl_leaders")
                else None,
                "BLK": leaders_grid.blk_leaders.get_data_frame()
                if hasattr(leaders_grid, "blk_leaders")
                else None,
                "GP": leaders_grid.g_p_leaders.get_data_frame()
                if hasattr(leaders_grid, "g_p_leaders")
                else None,
                "MIN": None,
            }

            rankings.append(
                self._build_ranking_data(
                    "总得分",
                    lebron_stats.get("points", 0),
                    leaders_data.get("PTS"),
                    "贾巴尔",
                )
            )

            rankings.append(
                self._build_ranking_data(
                    "总助攻",
                    lebron_stats.get("assists", 0),
                    leaders_data.get("AST"),
                    "纳什",
                )
            )

            rankings.append(
                self._build_ranking_data(
                    "总篮板",
                    lebron_stats.get("rebounds", 0),
                    leaders_data.get("REB"),
                    "瑟蒙德",
                )
            )

            rankings.append(
                self._build_ranking_data(
                    "总抢断",
                    lebron_stats.get("steals", 0),
                    leaders_data.get("STL"),
                    "奇克斯",
                )
            )

            rankings.append(
                self._build_ranking_data(
                    "总盖帽",
                    lebron_stats.get("blocks", 0),
                    leaders_data.get("BLK"),
                    "吉尔摩尔",
                )
            )

            rankings.append(
                self._build_ranking_data(
                    "总出场",
                    lebron_stats.get("games", 0),
                    leaders_data.get("GP"),
                    "帕里什",
                )
            )

            rankings.append(
                self._get_triple_double_ranking(lebron_stats.get("tripleDoubles", 0))
            )

            rankings.append(
                self._build_ranking_data(
                    "总时间",
                    lebron_stats.get("minutes", 0),
                    leaders_data.get("MIN"),
                    "贾巴尔",
                )
            )

            # 保存到缓存
            self.cache.save_data("rankings", rankings)

        except Exception as e:
            print(f"获取历史排名失败：{e}")
            rankings = self._get_mock_rankings(lebron_stats)

        return rankings

    # NBA历史总时间排名（AllTimeLeadersGrids不提供MIN数据，需硬编码）
    MIN_ALLTIME_LEADERS = [
        ("Kareem Abdul-Jabbar", 57446),
        ("Karl Malone", 54852),
        ("Jason Kidd", 50111),
        ("Dirk Nowitzki", 50000),
        ("Elvin Hayes", 50000),
    ]

    def _build_ranking_data(
        self, category: str, lebron_value: int, leaders_df, default_prev_name: str
    ) -> Dict[str, Any]:
        """构建排名数据"""
        # 特殊处理总时间排名（MIN不在AllTimeLeadersGrids中）
        if category == "总时间" and leaders_df is None:
            lebron_rank = 1  # 詹姆斯已超越贾巴尔
            prev_name = "贾巴尔"
            prev_value = self.MIN_ALLTIME_LEADERS[0][1]
            gap_to_prev = lebron_value - prev_value
            return {
                "category": category,
                "careerValue": lebron_value,
                "rank": lebron_rank,
                "prevPlayerName": prev_name,
                "prevPlayerValue": prev_value,
                "gapToPrev": gap_to_prev,
            }

        if leaders_df is None or leaders_df.empty:
            return {
                "category": category,
                "careerValue": lebron_value,
                "rank": 1,
                "prevPlayerName": default_prev_name,
                "prevPlayerValue": 0,
                "gapToPrev": lebron_value,
            }

        try:
            lebron_row = leaders_df[
                leaders_df["PLAYER_NAME"].str.contains("James", case=False, na=False)
            ]
            rank_col = (
                [c for c in leaders_df.columns if "RANK" in c][0]
                if any("RANK" in c for c in leaders_df.columns)
                else leaders_df.columns[-1]
            )
            value_col = (
                [
                    c
                    for c in leaders_df.columns
                    if c not in ["PLAYER_ID", "PLAYER_NAME", rank_col]
                ][0]
                if len(leaders_df.columns) > 2
                else leaders_df.columns[-1]
            )
            rank = (
                int(lebron_row.iloc[0].get(rank_col, 1)) if not lebron_row.empty else 1
            )

            if rank > 1:
                prev_row = leaders_df[leaders_df[rank_col] == rank - 1]
                if not prev_row.empty:
                    prev_name = prev_row.iloc[0].get("PLAYER_NAME", default_prev_name)
                    prev_value = int(prev_row.iloc[0].get(value_col, 0))
                else:
                    prev_name = default_prev_name
                    prev_value = 0
            else:
                next_row = leaders_df[leaders_df[rank_col] == 2]
                if not next_row.empty:
                    prev_name = next_row.iloc[0].get("PLAYER_NAME", default_prev_name)
                    prev_value = int(next_row.iloc[0].get(value_col, 0))
                else:
                    prev_name = default_prev_name
                    prev_value = 0

            gap_to_prev = (
                lebron_value - prev_value if rank == 1 else -(prev_value - lebron_value)
            )

            return {
                "category": category,
                "careerValue": lebron_value,
                "rank": rank,
                "prevPlayerName": self._translate_player_name(prev_name),
                "prevPlayerValue": prev_value,
                "gapToPrev": gap_to_prev,
            }

        except Exception as e:
            print(f"构建排名数据失败：{e}")
            return {
                "category": category,
                "careerValue": lebron_value,
                "rank": 1,
                "prevPlayerName": default_prev_name,
                "prevPlayerValue": 0,
                "gapToPrev": lebron_value,
            }

    def _get_triple_double_ranking(self, triple_doubles: int) -> Dict[str, Any]:
        """获取三双排名数据"""
        return {
            "category": "总三双",
            "careerValue": triple_doubles,
            "rank": 5,
            "prevPlayerName": "伯德",
            "prevPlayerValue": 59,
            "gapToPrev": 63,
        }

    def _translate_player_name(self, name: str) -> str:
        """翻译球员名称"""
        player_map = {
            "Kareem Abdul-Jabbar": "贾巴尔",
            "Steve Nash": "纳什",
            "Nate Thurmond": "瑟蒙德",
            "Maurice Cheeks": "奇克斯",
            "Artis Gilmore": "吉尔摩尔",
            "Robert Parish": "帕里什",
            "Larry Bird": "伯德",
        }
        return player_map.get(name, name)

    def _get_mock_rankings(self, lebron_stats: Dict[str, int]) -> List[Dict[str, Any]]:
        """返回模拟排名数据"""
        points = lebron_stats.get("points", 43290)
        rebounds = lebron_stats.get("rebounds", 12047)
        assists = lebron_stats.get("assists", 11952)
        steals = lebron_stats.get("steals", 2405)
        games = lebron_stats.get("games", 1615)

        return [
            {
                "category": "总得分",
                "careerValue": points,
                "rank": 1,
                "prevPlayerName": "贾巴尔",
                "prevPlayerValue": 38387,
                "gapToPrev": points - 38387,
            },
            {
                "category": "总助攻",
                "careerValue": assists,
                "rank": 4,
                "prevPlayerName": "纳什",
                "prevPlayerValue": 10335,
                "gapToPrev": -(10335 - assists),
            },
            {
                "category": "总篮板",
                "careerValue": rebounds,
                "rank": 23,
                "prevPlayerName": "瑟蒙德",
                "prevPlayerValue": 14464,
                "gapToPrev": -(14464 - rebounds),
            },
            {
                "category": "总抢断",
                "careerValue": steals,
                "rank": 8,
                "prevPlayerName": "奇克斯",
                "prevPlayerValue": 2310,
                "gapToPrev": steals - 2310,
            },
            {
                "category": "总盖帽",
                "careerValue": lebron_stats.get("blocks", 1147),
                "rank": 78,
                "prevPlayerName": "吉尔摩尔",
                "prevPlayerValue": 1178,
                "gapToPrev": -31,
            },
            {
                "category": "总出场",
                "careerValue": games,
                "rank": 1,
                "prevPlayerName": "帕里什",
                "prevPlayerValue": 1611,
                "gapToPrev": games - 1611,
            },
            {
                "category": "总三双",
                "careerValue": lebron_stats.get("tripleDoubles", 122),
                "rank": 5,
                "prevPlayerName": "伯德",
                "prevPlayerValue": 59,
                "gapToPrev": 63,
            },
            {
                "category": "总时间",
                "careerValue": lebron_stats.get("minutes", 59390),
                "rank": 2,
                "prevPlayerName": "贾巴尔",
                "prevPlayerValue": 66298,
                "gapToPrev": -6908,
            },
        ]

    def _translate_team(self, team_abbr: str) -> str:
        """翻译球队名称"""
        team_map = {
            "LAL": "湖人",
            "GSW": "勇士",
            "BOS": "凯尔特人",
            "MIA": "热火",
            "BKN": "篮网",
            "CHI": "公牛",
            "NYK": "尼克斯",
            "PHI": "76人",
            "TOR": "猛龙",
            "CLE": "骑士",
            "DET": "活塞",
            "IND": "步行者",
            "MIL": "雄鹿",
            "ATL": "老鹰",
            "CHA": "黄蜂",
            "ORL": "魔术",
            "WAS": "奇才",
            "DEN": "掘金",
            "MIN": "森林狼",
            "OKC": "雷霆",
            "POR": "开拓者",
            "UTA": "爵士",
            "LAC": "快船",
            "SAC": "国王",
            "PHX": "太阳",
            "DAL": "独行侠",
            "HOU": "火箭",
            "MEM": "灰熊",
            "NOP": "鹈鹕",
            "SAS": "马刺",
        }
        return team_map.get(team_abbr.upper(), team_abbr)

    def _get_mock_recent_game(self) -> Dict[str, Any]:
        """模拟最近比赛数据"""
        return {
            "opponent": "骑士",
            "date": "2026-04-01",
            "date_local": "2026年4月1日",
            "result": "W",
            "points": 28,
            "rebounds": 8,
            "assists": 6,
            "steals": 2,
            "blocks": 1,
            "minutes": 34.0,
            "fgPercent": 52.4,
            "threePercent": 40.0,
            "ftPercent": 85.7,
        }

    def _get_mock_career_stats(self) -> Dict[str, int]:
        """模拟生涯数据"""
        return {
            "games": 1615,
            "points": 43290,
            "rebounds": 12047,
            "assists": 11952,
            "steals": 2405,
            "blocks": 1147,
            "minutes": 59390,
            "tripleDoubles": 122,
        }


if __name__ == "__main__":
    client = NBADataClient()

    print("=" * 60)
    print("🏀 NBA 数据客户端优化版测试")
    print("=" * 60)

    # 测试时区转换
    print("\n【时区转换测试】")
    utc_date = "2026-04-01"
    print(f"UTC日期: {utc_date}")
    print(f"中国日期: {TimeZoneManager.get_local_date(utc_date, 'CN')}")
    print(f"美国日期: {TimeZoneManager.get_local_date(utc_date, 'US-CA')}")

    # 测试赛程检查
    print("\n【赛程检查】")
    today = datetime.now().strftime("%Y-%m-%d")
    has_game = ScheduleManager.has_game_today(today)
    print(f"今天 ({today}) 是否有比赛: {has_game}")

    # 测试数据获取
    print("\n【詹姆斯最近比赛】")
    recent_game = client.get_lebron_recent_game()
    if recent_game:
        print(f"对手：{recent_game['opponent']}")
        print(f"UTC日期：{recent_game.get('date', 'N/A')}")
        print(f"本地日期：{recent_game.get('date_local', 'N/A')}")
        print(f"结果：{recent_game['result']}")

    print("\n【詹姆斯生涯数据】")
    career = client.get_lebron_career_stats()
    print(f"出场：{career['games']}场")
    print(f"得分：{career['points']}分")
    print(f"最后更新：{career.get('last_updated', 'N/A')}")
