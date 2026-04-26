"""
数据校验模块 - 确保缓存数据与NBA API实时数据一致
以NBA API数据为准，提供数据对比和验证功能
"""

from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime, timedelta
import json


class DataValidator:
    """数据校验器 - 对比缓存数据与API数据，以API为准"""

    def __init__(self):
        self.validation_results = []

    def validate_game_data(
        self, cached_data: Optional[Dict], api_data: Optional[Dict]
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        校验比赛数据

        Args:
            cached_data: 缓存的比赛数据
            api_data: 从NBA API获取的实时数据

        Returns:
            (是否需要更新, 最终数据, 校验说明)
        """
        # 如果没有API数据，使用缓存（如果存在）
        if not api_data:
            if cached_data:
                return False, cached_data, "API数据为空，使用缓存数据"
            else:
                return False, None, "API和缓存数据均为空"

        # 如果没有缓存数据，直接使用API数据
        if not cached_data:
            return True, api_data, "无缓存数据，使用API数据"

        # 对比关键字段
        differences = self._compare_game_fields(cached_data, api_data)

        if not differences:
            return False, api_data, "缓存与API数据完全一致"

        # 记录差异
        print(f"[数据校验] 发现 {len(differences)} 处差异：")
        for diff in differences:
            print(f"  - {diff['field']}: 缓存={diff['cached']}, API={diff['api']}")

        # 以API数据为准
        return True, api_data, f"发现{len(differences)}处差异，使用API数据覆盖缓存"

    def _compare_game_fields(self, cached: Dict, api: Dict) -> List[Dict[str, Any]]:
        """对比比赛数据字段"""
        differences = []

        # 关键字段列表
        key_fields = [
            "date",
            "opponent",
            "result",
            "points",
            "rebounds",
            "assists",
            "steals",
            "blocks",
            "minutes",
            "fgPercent",
            "threePercent",
            "ftPercent",
        ]

        for field in key_fields:
            cached_val = cached.get(field)
            api_val = api.get(field)

            # 数值字段允许小幅度差异（浮点数精度问题）
            if field.endswith("Percent") or field in ["minutes"]:
                if not self._float_equal(cached_val, api_val, tolerance=0.1):
                    differences.append(
                        {
                            "field": field,
                            "cached": cached_val,
                            "api": api_val,
                            "type": "float_diff",
                        }
                    )
            elif cached_val != api_val:
                differences.append(
                    {
                        "field": field,
                        "cached": cached_val,
                        "api": api_val,
                        "type": "diff",
                    }
                )

        return differences

    def _float_equal(self, a, b, tolerance=0.01) -> bool:
        """比较两个浮点数是否在误差范围内相等"""
        try:
            return abs(float(a) - float(b)) <= tolerance
        except (ValueError, TypeError):
            return a == b

    def validate_career_stats(
        self, cached_data: Optional[Dict], api_data: Optional[Dict]
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        校验生涯统计数据

        Args:
            cached_data: 缓存的生涯数据
            api_data: 从NBA API获取的实时数据

        Returns:
            (是否需要更新, 最终数据, 校验说明)
        """
        # 如果没有API数据，使用缓存
        if not api_data:
            if cached_data:
                return False, cached_data, "API数据为空，使用缓存数据"
            else:
                return False, None, "API和缓存数据均为空"

        # 如果没有缓存数据，直接使用API数据
        if not cached_data:
            return True, api_data, "无缓存数据，使用API数据"

        # 对比关键统计字段
        differences = self._compare_career_fields(cached_data, api_data)

        if not differences:
            return False, api_data, "缓存与API数据完全一致"

        # 记录差异
        print(f"[数据校验] 生涯数据发现 {len(differences)} 处差异：")
        for diff in differences:
            print(f"  - {diff['field']}: 缓存={diff['cached']}, API={diff['api']}")

        # 验证逻辑：API数据应该 >= 缓存数据（生涯累计只增不减）
        validated_data = self._validate_career_progression(cached_data, api_data)

        if validated_data != api_data:
            print(f"[数据校验] 生涯数据异常，进行修正")
            return True, validated_data, "检测到异常数据，已修正"

        return True, api_data, f"发现{len(differences)}处差异，使用API数据"

    def _compare_career_fields(self, cached: Dict, api: Dict) -> List[Dict[str, Any]]:
        """对比生涯数据字段"""
        differences = []

        # 关键统计字段（只增不减的字段）
        stat_fields = [
            "games",
            "points",
            "rebounds",
            "assists",
            "steals",
            "blocks",
            "minutes",
        ]

        for field in stat_fields:
            cached_val = cached.get(field, 0)
            api_val = api.get(field, 0)

            if cached_val != api_val:
                differences.append(
                    {"field": field, "cached": cached_val, "api": api_val}
                )

        return differences

    def _validate_career_progression(self, cached: Dict, api: Dict) -> Dict[str, Any]:
        """
        验证生涯数据的合理性（只增不减）

        如果API数据 < 缓存数据，说明可能获取了不完整数据，
        此时应该使用较大的值（通常是缓存值）
        """
        result = api.copy()

        stat_fields = [
            "games",
            "points",
            "rebounds",
            "assists",
            "steals",
            "blocks",
            "minutes",
        ]

        for field in stat_fields:
            cached_val = cached.get(field, 0)
            api_val = api.get(field, 0)

            # 如果API数据小于缓存数据，可能是API返回了不完整数据
            if api_val < cached_val:
                print(
                    f"[数据校验] 警告：{field} API数据({api_val}) < 缓存({cached_val})，使用缓存值"
                )
                result[field] = cached_val

        return result

    def get_validation_summary(self) -> Dict[str, Any]:
        """获取校验结果摘要"""
        return {
            "total_validations": len(self.validation_results),
            "last_validation": (
                self.validation_results[-1] if self.validation_results else None
            ),
            "validation_history": self.validation_results[-10:],  # 最近10次
        }


class RealTimeDataChecker:
    """实时数据检查器 - 定期检查数据更新"""

    def __init__(self, data_client):
        self.data_client = data_client
        self.last_check_time = None
        self.check_interval = timedelta(minutes=5)  # 默认5分钟检查一次

    def should_check_update(self) -> bool:
        """判断是否应该检查更新"""
        if not self.last_check_time:
            return True

        return datetime.now() - self.last_check_time >= self.check_interval

    def check_game_update(self) -> Dict[str, Any]:
        """检查比赛数据是否有更新"""
        self.last_check_time = datetime.now()

        try:
            # 获取当前缓存
            cached = self.data_client.cache.load_data("recent_game")

            # 强制从API获取最新数据（跳过缓存）
            api_data = self._fetch_latest_game_from_api()

            if not api_data:
                return {"updated": False, "reason": "API返回空数据", "data": cached}

            # 对比数据
            if cached:
                if api_data.get("date") != cached.get("date"):
                    return {
                        "updated": True,
                        "reason": "发现新比赛",
                        "old_date": cached.get("date"),
                        "new_date": api_data.get("date"),
                        "data": api_data,
                    }
                elif api_data != cached:
                    return {
                        "updated": True,
                        "reason": "比赛数据有更新",
                        "data": api_data,
                    }
                else:
                    return {"updated": False, "reason": "数据一致", "data": api_data}
            else:
                return {"updated": True, "reason": "首次获取数据", "data": api_data}

        except Exception as e:
            return {"updated": False, "reason": f"检查失败: {str(e)}", "data": None}

    def _fetch_latest_game_from_api(self) -> Optional[Dict]:
        """强制从API获取最新比赛数据"""
        # 临时禁用缓存读取，直接调用API
        original_cache = self.data_client.cache
        try:
            # 创建一个不读取缓存的获取方法
            # 这里需要直接调用底层的API获取逻辑
            game_data = self._fetch_without_cache()
            return game_data
        except Exception as e:
            print(f"[实时检查] API获取失败: {e}")
            return None

    def _fetch_without_cache(self) -> Optional[Dict]:
        """不经过缓存直接获取API数据"""
        from nba_api.stats.endpoints import playergamelog

        # 动态获取当前赛季
        current_year = datetime.now().year
        season = f"{current_year}-{str(current_year + 1)[-2:]}"

        gamelog = playergamelog.PlayerGameLog(
            player_id="2544",
            season=season,
            season_type_all_star="Regular Season",
        )

        games = gamelog.player_game_log.get_data_frame()

        if games.empty:
            return None

        last_game = games.iloc[0]

        return {
            "opponent": last_game.get("MATCHUP", "").split()[-1],
            "date": str(last_game.get("GAME_DATE", "")),
            "result": last_game.get("WL", ""),
            "points": int(last_game.get("PTS", 0)),
            "rebounds": int(last_game.get("REB", 0)),
            "assists": int(last_game.get("AST", 0)),
            "steals": int(last_game.get("STL", 0)),
            "blocks": int(last_game.get("BLK", 0)),
            "minutes": float(last_game.get("MIN", 0)),
            "fgPercent": round(float(last_game.get("FG_PCT", 0)) * 100, 1),
            "threePercent": round(float(last_game.get("FG3_PCT", 0)) * 100, 1),
            "ftPercent": round(float(last_game.get("FT_PCT", 0)) * 100, 1),
        }
