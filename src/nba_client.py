"""
NBA API 客户端 - 真实数据版
使用 nba_api 库接入 NBA.com 官方 API
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta

NBA_API_AVAILABLE = False

try:
    from nba_api.stats.endpoints import playercareerstats, playergamelog, scoreboard
    from nba_api.stats.static import players, teams
    from nba_api.live.nba.endpoints import scoreboard as live_scoreboard
    NBA_API_AVAILABLE = True
except Exception as e:
    pass  # 静默失败，使用模拟数据


class NBAClient:
    """NBA 数据客户端（真实 API 版）"""
    
    def __init__(self, provider: str = "nba"):
        """
        初始化客户端
        
        Args:
            provider: API 提供商 (nba | mock)
        """
        self.provider = provider if NBA_API_AVAILABLE else "mock"
    
    def get_teams(self) -> List[Dict]:
        """获取球队列表"""
        if self.provider == "nba" and NBA_API_AVAILABLE:
            try:
                nba_teams = teams.get_teams()
                return nba_teams
            except Exception as e:
                print(f"获取球队数据失败：{e}")
                return self._get_mock_teams()
        return self._get_mock_teams()
    
    def get_today_games(self) -> List[Dict]:
        """获取今日比赛"""
        if self.provider == "nba" and NBA_API_AVAILABLE:
            try:
                games = live_scoreboard.ScoreBoard()
                game_data = games.get_dict()
                
                if 'games' in game_data:
                    return game_data['games']
                return []
            except Exception as e:
                print(f"获取今日比赛失败：{e}")
                return []
        return self._get_mock_games()
    
    def get_yesterday_games(self) -> List[Dict]:
        """获取昨日比赛"""
        if self.provider == "nba" and NBA_API_AVAILABLE:
            try:
                # 计算昨天日期
                yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
                
                games = scoreboard.ScoreBoard(date=yesterday)
                game_data = games.get_dict()
                
                if 'games' in game_data:
                    return game_data['games']
                return []
            except Exception as e:
                print(f"获取昨日比赛失败：{e}")
                return []
        return self._get_mock_games()
    
    def get_players(self, search: Optional[str] = None) -> List[Dict]:
        """获取球员列表"""
        if self.provider == "nba" and NBA_API_AVAILABLE:
            try:
                if search:
                    player_dict = players.find_players_by_full_name(search)
                    return player_dict if player_dict else []
                else:
                    # 获取所有球员（可能需要分页）
                    all_players = players.get_players()
                    return all_players[:100]  # 限制返回数量
            except Exception as e:
                print(f"获取球员数据失败：{e}")
                return []
        return self._get_mock_players(search)
    
    def get_player_by_name(self, name: str) -> Optional[Dict]:
        """
        根据姓名获取球员
        
        Args:
            name: 球员姓名
            
        Returns:
            球员信息
        """
        if self.provider == "nba" and NBA_API_AVAILABLE:
            try:
                player_dict = players.find_players_by_full_name(name)
                if player_dict:
                    return player_dict[0]
                return None
            except Exception as e:
                print(f"查找球员失败：{e}")
                return None
        return None
    
    def get_player_career_stats(self, player_id: str) -> Dict:
        """
        获取球员生涯数据
        
        Args:
            player_id: 球员 ID
            
        Returns:
            生涯统计数据
        """
        if self.provider == "nba" and NBA_API_AVAILABLE:
            try:
                career = playercareerstats.PlayerCareerStats(player_id=player_id)
                
                # 常规赛数据
                regular_season = career.season_totals_regular_season.get_data_frame()
                
                # 季后赛数据
                playoff_season = career.season_totals_post_season.get_data_frame()
                
                career_stats = {
                    'seasons_played': len(regular_season),
                    'regular_season': {
                        'games': int(regular_season['GP'].sum()) if len(regular_season) > 0 else 0,
                        'points': int(regular_season['PTS'].sum()) if len(regular_season) > 0 else 0,
                        'rebounds': int(regular_season['REB'].sum()) if len(regular_season) > 0 else 0,
                        'assists': int(regular_season['AST'].sum()) if len(regular_season) > 0 else 0,
                        'steals': int(regular_season['STL'].sum()) if len(regular_season) > 0 else 0,
                        'blocks': int(regular_season['BLK'].sum()) if len(regular_season) > 0 else 0,
                        'ppg': float(regular_season['PTS'].mean()) if len(regular_season) > 0 else 0,
                        'rpg': float(regular_season['REB'].mean()) if len(regular_season) > 0 else 0,
                        'apg': float(regular_season['AST'].mean()) if len(regular_season) > 0 else 0,
                    },
                    'playoffs': {
                        'games': int(playoff_season['GP'].sum()) if len(playoff_season) > 0 else 0,
                        'points': int(playoff_season['PTS'].sum()) if len(playoff_season) > 0 else 0,
                        'rebounds': int(playoff_season['REB'].sum()) if len(playoff_season) > 0 else 0,
                        'assists': int(playoff_season['AST'].sum()) if len(playoff_season) > 0 else 0,
                    }
                }
                
                return career_stats
            except Exception as e:
                print(f"获取生涯数据失败：{e}")
                return {}
        return {}
    
    def get_player_recent_games(self, player_id: str, season: str = "2025-26", num_games: int = 10) -> List[Dict]:
        """
        获取球员最近比赛数据
        
        Args:
            player_id: 球员 ID
            season: 赛季 (如 2025-26)
            num_games: 比赛场次数
            
        Returns:
            比赛数据列表
        """
        if self.provider == "nba" and NBA_API_AVAILABLE:
            try:
                import pandas as pd
                
                game_log = playergamelog.PlayerGameLog(
                    player_id=player_id,
                    season=season,
                    season_type_all_star=['Regular Season']
                )
                
                data = game_log.get_dict()
                
                if 'resultSets' in data and len(data['resultSets']) > 0:
                    df = pd.DataFrame(
                        data['resultSets'][0]['rowSet'],
                        columns=data['resultSets'][0]['headers']
                    )
                    
                    recent_games = []
                    for _, row in df.head(num_games).iterrows():
                        game = {
                            'date': row['GAME_DATE'],
                            'matchup': row['MATCHUP'],
                            'result': row['WL'],
                            'minutes': float(row['MIN']) if row['MIN'] else 0,
                            'points': int(row['PTS']) if row['PTS'] else 0,
                            'rebounds': int(row['REB']) if row['REB'] else 0,
                            'assists': int(row['AST']) if row['AST'] else 0,
                            'steals': int(row['STL']) if row['STL'] else 0,
                            'blocks': int(row['BLK']) if row['BLK'] else 0,
                            'turnovers': int(row['TOV']) if row['TOV'] else 0,
                            'fg_pct': float(row['FG_PCT']) if row['FG_PCT'] else 0,
                            'fg3_pct': float(row['FG3_PCT']) if row['FG3_PCT'] else 0,
                            'ft_pct': float(row['FT_PCT']) if row['FT_PCT'] else 0,
                            'plus_minus': int(row['PLUS_MINUS']) if row['PLUS_MINUS'] else 0
                        }
                        recent_games.append(game)
                    
                    return recent_games
                return []
            except Exception as e:
                print(f"获取比赛数据失败：{e}")
                return []
        return []
    
    def search_player(self, name: str) -> List[Dict]:
        """搜索球员"""
        return self.get_players(search=name)
    
    def get_team_by_name(self, name: str) -> Optional[Dict]:
        """根据名称获取球队"""
        teams_list = self.get_teams()
        for team in teams_list:
            if name.lower() in team['full_name'].lower() or name.lower() in team['name'].lower():
                return team
        return None
    
    # 模拟数据（备用）
    def _get_mock_teams(self) -> List[Dict]:
        """获取模拟球队数据"""
        return [
            {"id": 1, "abbreviation": "LAL", "city": "Los Angeles", "conference": "West",
             "division": "Pacific", "full_name": "Los Angeles Lakers", "name": "Lakers"},
            {"id": 2, "abbreviation": "GSW", "city": "Golden State", "conference": "West",
             "division": "Pacific", "full_name": "Golden State Warriors", "name": "Warriors"},
            {"id": 3, "abbreviation": "BOS", "city": "Boston", "conference": "East",
             "division": "Atlantic", "full_name": "Boston Celtics", "name": "Celtics"},
        ]
    
    def _get_mock_games(self) -> List[Dict]:
        """获取模拟比赛数据"""
        return [
            {
                "id": 1001,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "home_team": {"id": 1, "abbreviation": "LAL", "full_name": "Los Angeles Lakers"},
                "visitor_team": {"id": 2, "abbreviation": "GSW", "full_name": "Golden State Warriors"},
                "home_team_score": 112,
                "visitor_team_score": 108,
                "status": "Final",
            },
        ]
    
    def _get_mock_players(self, search: Optional[str] = None) -> List[Dict]:
        """获取模拟球员数据"""
        players = [
            {"id": 2544, "first_name": "LeBron", "last_name": "James", "position": "F",
             "team": {"id": 1, "abbreviation": "LAL", "full_name": "Los Angeles Lakers"}},
            {"id": 201939, "first_name": "Stephen", "last_name": "Curry", "position": "G",
             "team": {"id": 2, "abbreviation": "GSW", "full_name": "Golden State Warriors"}},
        ]
        
        if search:
            return [p for p in players if search.lower() in p['first_name'].lower() or 
                   search.lower() in p['last_name'].lower()]
        return players


# 测试
if __name__ == "__main__":
    client = NBAClient(provider="nba")
    
    print("🏀 测试 NBA API 客户端（真实数据）\n")
    
    # 获取球队
    print("【NBA 球队】")
    teams = client.get_teams()
    print(f"  共 {len(teams)} 支球队")
    for team in teams[:5]:
        print(f"  - {team['full_name']} ({team['abbreviation']})")
    print()
    
    # 获取今日比赛
    print("【今日比赛】")
    games = client.get_today_games()
    if games:
        print(f"  共 {len(games)} 场比赛")
        for game in games[:3]:
            home = game['homeTeam'] if 'homeTeam' in game else game.get('home_team', {})
            visitor = game['visitorTeam'] if 'visitorTeam' in game else game.get('visitor_team', {})
            home_score = game.get('homeTeamScore', 0)
            visitor_score = game.get('visitorTeamScore', 0)
            print(f"  {visitor.get('fullName', 'N/A')} @ {home.get('fullName', 'N/A')}")
            if home_score and visitor_score:
                print(f"    比分：{visitor_score} - {home_score}")
    else:
        print("  今天没有比赛")
    print()
    
    # 搜索球员
    print("【搜索球员：LeBron James】")
    players = client.search_player("LeBron James")
    if players:
        player = players[0]
        print(f"  ✅ 找到：{player['first_name']} {player['last_name']}")
        print(f"     ID: {player['id']}")
        print(f"     球队：{player.get('team', {}).get('full_name', 'N/A')}")
        
        # 获取生涯数据
        print("\n【生涯数据】")
        career_stats = client.get_player_career_stats(player['id'])
        if career_stats:
            print(f"  效力赛季：{career_stats.get('seasons_played', 0)} 个")
            print(f"  常规赛总得分：{career_stats['regular_season']['points']:,} 分")
            print(f"  常规赛总篮板：{career_stats['regular_season']['rebounds']:,} 个")
            print(f"  常规赛总助攻：{career_stats['regular_season']['assists']:,} 次")
    else:
        print("  未找到球员")
    print()
