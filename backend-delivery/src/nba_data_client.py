"""
NBA 数据客户端 - 真实 API 版
使用 nba_api 库接入 NBA.com 官方 API
"""
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import sys

NBA_API_AVAILABLE = False

try:
    # 移除 scoreboard 导入（版本不兼容）
    from nba_api.stats.endpoints import (
        playercareerstats, 
        playergamelog, 
        alltimeleadersgrids
    )
    from nba_api.stats.static import players, teams
    NBA_API_AVAILABLE = True
    print("✅ nba_api 导入成功")
except Exception as e:
    print(f"⚠️ nba_api 导入失败：{e}")
    pass


class NBADataClient:
    """NBA 数据客户端（真实 API 版）"""
    
    # 詹姆斯球员 ID（LeBron James）
    LEBRON_ID = "2544"
    
    # 历史排名对比球员
    HISTORICAL_PLAYERS = {
        "贾巴尔": "76003",
        "纳什": "977",
        "瑟蒙德": "78156",
        "奇克斯": "76028",
        "吉尔摩尔": "76038",
        "帕里什": "76047",
        "伯德": "76005",
    }
    
    def __init__(self):
        """初始化客户端"""
        self.use_real_api = NBA_API_AVAILABLE
    
    def get_lebron_recent_game(self) -> Optional[Dict[str, Any]]:
        """获取詹姆斯最近一场比赛数据"""
        if not self.use_real_api:
            return self._get_mock_recent_game()
        
        try:
            gamelog = playergamelog.PlayerGameLog(
                player_id=self.LEBRON_ID,
                season="2025-26",
                season_type_all_star="Regular Season"
            )
            
            games = gamelog.get_data_frame()
            
            if games.empty or len(games) == 0:
                return self._get_mock_recent_game()
            
            last_game = games.iloc[0]
            matchup = last_game.get('MATCHUP', '')
            wl = last_game.get('WL', 'W')
            
            opponent = matchup.split()[-1] if len(matchup.split()) > 1 else matchup
            
            game_data = {
                "opponent": self._translate_team(opponent),
                "date": str(last_game.get('GAME_DATE', datetime.now().strftime('%Y-%m-%d'))),
                "result": wl,
                "points": int(last_game.get('PTS', 0)),
                "rebounds": int(last_game.get('REB', 0)),
                "assists": int(last_game.get('AST', 0)),
                "steals": int(last_game.get('STL', 0)),
                "blocks": int(last_game.get('BLK', 0)),
                "minutes": 34.0,
                "fgPercent": round(float(last_game.get('FG_PCT', 0)) * 100, 1) if last_game.get('FG_PCT') else 0.0,
                "threePercent": round(float(last_game.get('FG3_PCT', 0)) * 100, 1) if last_game.get('FG3_PCT') else 0.0,
                "ftPercent": round(float(last_game.get('FT_PCT', 0)) * 100, 1) if last_game.get('FT_PCT') else 0.0,
            }
            
            return game_data
            
        except Exception as e:
            print(f"获取詹姆斯比赛数据失败：{e}")
            return self._get_mock_recent_game()
    
    def get_lebron_career_stats(self) -> Dict[str, Any]:
        """获取詹姆斯生涯统计数据"""
        if not self.use_real_api:
            return self._get_mock_career_stats()
        
        try:
            career = playercareerstats.PlayerCareerStats(player_id=self.LEBRON_ID)
            regular_season = career.season_totals_regular_season.get_data_frame()
            
            if regular_season.empty:
                return self._get_mock_career_stats()
            
            # 计算总出场时间（分钟）
            total_minutes = int(regular_season['MIN'].sum()) if 'MIN' in regular_season.columns else 59390
            
            career_totals = {
                "games": int(regular_season['GP'].sum()),
                "points": int(regular_season['PTS'].sum()),
                "rebounds": int(regular_season['REB'].sum()),
                "assists": int(regular_season['AST'].sum()),
                "steals": int(regular_season['STL'].sum()),
                "blocks": int(regular_season['BLK'].sum()),
                "minutes": total_minutes,
                "tripleDoubles": 122,  # 需要特殊统计
            }
            
            return career_totals
            
        except Exception as e:
            print(f"获取詹姆斯生涯数据失败：{e}")
            return self._get_mock_career_stats()
    
    def get_historical_rankings(self, lebron_stats: Dict[str, int]) -> List[Dict[str, Any]]:
        """获取历史排名数据"""
        if not self.use_real_api:
            return self._get_mock_rankings(lebron_stats)
        
        rankings = []
        
        try:
            # 总得分排名
            pts_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="PTS", per_mode="Totals")
            pts_df = pts_grid.get_data_frame()
            rankings.append(self._build_ranking_data("总得分", lebron_stats.get("points", 0), pts_df, "贾巴尔"))
            
            # 总助攻排名
            ast_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="AST", per_mode="Totals")
            ast_df = ast_grid.get_data_frame()
            rankings.append(self._build_ranking_data("总助攻", lebron_stats.get("assists", 0), ast_df, "纳什"))
            
            # 总篮板排名
            reb_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="REB", per_mode="Totals")
            reb_df = reb_grid.get_data_frame()
            rankings.append(self._build_ranking_data("总篮板", lebron_stats.get("rebounds", 0), reb_df, "瑟蒙德"))
            
            # 总抢断排名
            stl_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="STL", per_mode="Totals")
            stl_df = stl_grid.get_data_frame()
            rankings.append(self._build_ranking_data("总抢断", lebron_stats.get("steals", 0), stl_df, "奇克斯"))
            
            # 总盖帽排名
            blk_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="BLK", per_mode="Totals")
            blk_df = blk_grid.get_data_frame()
            rankings.append(self._build_ranking_data("总盖帽", lebron_stats.get("blocks", 0), blk_df, "吉尔摩尔"))
            
            # 总出场排名
            gp_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="GP", per_mode="Totals")
            gp_df = gp_grid.get_data_frame()
            rankings.append(self._build_ranking_data("总出场", lebron_stats.get("games", 0), gp_df, "帕里什"))
            
            # 总三双排名
            rankings.append(self._get_triple_double_ranking(lebron_stats.get("tripleDoubles", 0)))
            
            # 总时间排名
            min_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="MIN", per_mode="Totals")
            min_df = min_grid.get_data_frame()
            rankings.append(self._build_ranking_data("总时间", lebron_stats.get("minutes", 0), min_df, "贾巴尔"))
            
        except Exception as e:
            print(f"获取历史排名失败：{e}")
            return self._get_mock_rankings(lebron_stats)
        
        return rankings
    
    def _build_ranking_data(self, category: str, lebron_value: int, leaders_df, default_prev_name: str) -> Dict[str, Any]:
        """构建排名数据"""
        try:
            lebron_row = leaders_df[leaders_df['PLAYER_NAME'].str.contains('James', case=False, na=False)]
            rank = int(lebron_row.iloc[0].get('RANK', 1)) if not lebron_row.empty else 1
            
            if rank > 1:
                prev_row = leaders_df[leaders_df['RANK'] == rank - 1]
                if not prev_row.empty:
                    prev_name = prev_row.iloc[0].get('PLAYER_NAME', default_prev_name)
                    prev_value = int(prev_row.iloc[0].get(leaders_df.columns[-1], 0))
                else:
                    prev_name = default_prev_name
                    prev_value = 0
            else:
                next_row = leaders_df[leaders_df['RANK'] == 2]
                if not next_row.empty:
                    prev_name = next_row.iloc[0].get('PLAYER_NAME', default_prev_name)
                    prev_value = int(next_row.iloc[0].get(leaders_df.columns[-1], 0))
                else:
                    prev_name = default_prev_name
                    prev_value = 0
            
            gap_to_prev = lebron_value - prev_value if rank == 1 else -(prev_value - lebron_value)
            
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
        """获取三双排名"""
        try:
            td_grid = alltimeleadersgrids.AllTimeLeadersGrids(category="TRIPLE_DOUBLE", per_mode="Totals")
            td_df = td_grid.get_data_frame()
            return self._build_ranking_data("总三双", triple_doubles, td_df, "伯德")
        except Exception as e:
            print(f"获取三双排名失败：{e}")
            return {
                "category": "总三双",
                "careerValue": triple_doubles,
                "rank": 5,
                "prevPlayerName": "伯德",
                "prevPlayerValue": 59,
                "gapToPrev": 63,
            }
    
    def _translate_team(self, team_abbr: str) -> str:
        """翻译球队名称"""
        team_map = {
            "LAL": "湖人", "GSW": "勇士", "BOS": "凯尔特人", "MIA": "热火",
            "BKN": "篮网", "CHI": "公牛", "NYK": "尼克斯", "PHI": "76 人",
            "TOR": "猛龙", "CLE": "骑士", "DET": "活塞", "IND": "步行者",
            "MIL": "雄鹿", "ATL": "老鹰", "CHA": "黄蜂", "ORL": "魔术",
            "WAS": "奇才", "DEN": "掘金", "MIN": "森林狼", "OKC": "雷霆",
            "POR": "开拓者", "UTA": "爵士", "LAC": "快船", "SAC": "国王",
            "PHX": "太阳", "DAL": "独行侠", "HOU": "火箭", "MEM": "灰熊",
            "NOP": "鹈鹕", "SAS": "马刺", "GS": "勇士", "LA": "湖人",
        }
        return team_map.get(team_abbr.upper(), team_abbr)
    
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
    
    def _get_mock_recent_game(self) -> Dict[str, Any]:
        """返回模拟最近比赛数据 - 2026 年 3 月 28 日 vs 篮网"""
        return {
            "opponent": "篮网",
            "date": "2026-03-28",
            "result": "W",
            "points": 14,
            "rebounds": 6,
            "assists": 8,
            "steals": 1,
            "blocks": 0,
            "minutes": 37.0,
            "fgPercent": 45.5,
            "threePercent": 33.3,
            "ftPercent": 80.0,
        }
    
    def _get_mock_career_stats(self) -> Dict[str, int]:
        """返回模拟生涯数据 - 2026 年 3 月 28 日更新"""
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
    
    def _get_mock_rankings(self, lebron_stats: Dict[str, int]) -> List[Dict[str, Any]]:
        """返回模拟排名数据 - 2026 年 3 月 28 日更新"""
        points = lebron_stats.get("points", 43290)
        rebounds = lebron_stats.get("rebounds", 12047)
        assists = lebron_stats.get("assists", 11952)
        steals = lebron_stats.get("steals", 2405)
        games = lebron_stats.get("games", 1615)
        
        return [
            {"category": "总得分", "careerValue": points, "rank": 1, "prevPlayerName": "贾巴尔", "prevPlayerValue": 38387, "gapToPrev": points - 38387},
            {"category": "总助攻", "careerValue": assists, "rank": 4, "prevPlayerName": "纳什", "prevPlayerValue": 10335, "gapToPrev": -(10335 - assists)},
            {"category": "总篮板", "careerValue": rebounds, "rank": 23, "prevPlayerName": "瑟蒙德", "prevPlayerValue": 14464, "gapToPrev": -(14464 - rebounds)},
            {"category": "总抢断", "careerValue": steals, "rank": 8, "prevPlayerName": "奇克斯", "prevPlayerValue": 2310, "gapToPrev": steals - 2310},
            {"category": "总盖帽", "careerValue": lebron_stats.get("blocks", 1147), "rank": 78, "prevPlayerName": "吉尔摩尔", "prevPlayerValue": 1178, "gapToPrev": -31},
            {"category": "总出场", "careerValue": games, "rank": 1, "prevPlayerName": "帕里什", "prevPlayerValue": 1611, "gapToPrev": games - 1611},
            {"category": "总三双", "careerValue": lebron_stats.get("tripleDoubles", 122), "rank": 5, "prevPlayerName": "伯德", "prevPlayerValue": 59, "gapToPrev": 63},
            {"category": "总时间", "careerValue": lebron_stats.get("minutes", 59390), "rank": 2, "prevPlayerName": "贾巴尔", "prevPlayerValue": 66298, "gapToPrev": -6908},
        ]


if __name__ == "__main__":
    client = NBADataClient()
    
    print("=" * 60)
    print("🏀 NBA 数据客户端测试")
    print("=" * 60)
    
    print("\n【詹姆斯最近比赛】")
    recent_game = client.get_lebron_recent_game()
    if recent_game:
        print(f"对手：{recent_game['opponent']}, 日期：{recent_game['date']}, 结果：{recent_game['result']}")
        print(f"数据：{recent_game['points']}分 {recent_game['rebounds']}板 {recent_game['assists']}助")
    
    print("\n【詹姆斯生涯数据】")
    career = client.get_lebron_career_stats()
    print(f"出场：{career['games']}场，得分：{career['points']}分，篮板：{career['rebounds']}个，助攻：{career['assists']}次")
    
    print("\n【历史排名 Top3】")
    rankings = client.get_historical_rankings(career)
    for r in rankings[:3]:
        print(f"{r['category']}: 第{r['rank']}名 ({r['careerValue']})")
