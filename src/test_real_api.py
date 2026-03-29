#!/usr/bin/env python3
"""
测试真实 NBA API
"""
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats
from nba_api.live.nba.endpoints import scoreboard

print("="*60)
print("🏀 NBA 真实 API 测试")
print("="*60)
print()

# 1. 获取球队
print("【NBA 球队】")
nba_teams = teams.get_teams()
print(f"  共 {len(nba_teams)} 支球队")
for team in nba_teams[:5]:
    print(f"  - {team['full_name']} ({team['abbreviation']})")
print()

# 2. 搜索球员
print("【搜索球员：LeBron James】")
lebron = players.find_players_by_full_name('LeBron James')
if lebron:
    player = lebron[0]
    print(f"  ✅ 找到：{player['full_name']}")
    print(f"     ID: {player['id']}")
    print(f"     状态：{'活跃' if player['is_active'] else '退役'}")
    print()
    
    # 3. 获取生涯数据
    print("【生涯数据】")
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player['id'])
        regular_season = career.season_totals_regular_season.get_data_frame()
        
        total_points = int(regular_season['PTS'].sum())
        total_rebounds = int(regular_season['REB'].sum())
        total_assists = int(regular_season['AST'].sum())
        
        print(f"  效力赛季：{len(regular_season)} 个")
        print(f"  总得分：   {total_points:,} 分")
        print(f"  总篮板：   {total_rebounds:,} 个")
        print(f"  总助攻：   {total_assists:,} 次")
        print()
    except Exception as e:
        print(f"  ❌ 获取生涯数据失败：{e}")
        print()
else:
    print("  ❌ 未找到球员")
    print()

# 4. 今日比赛
print("【今日比赛】")
try:
    games = scoreboard.ScoreBoard()
    game_data = games.get_dict()
    
    if 'games' in game_data and len(game_data['games']) > 0:
        print(f"  共 {len(game_data['games'])} 场比赛")
        for game in game_data['games'][:3]:
            home = game.get('homeTeam', {})
            visitor = game.get('visitorTeam', {})
            home_score = game.get('homeTeamScore', 0)
            visitor_score = game.get('visitorTeamScore', 0)
            
            print(f"  {visitor.get('fullName', 'N/A')} @ {home.get('fullName', 'N/A')}")
            if home_score and visitor_score:
                print(f"    比分：{visitor_score} - {home_score}")
    else:
        print("  今天没有比赛")
except Exception as e:
    print(f"  ❌ 获取比赛失败：{e}")
print()

print("="*60)
print("✅ API 测试完成！")
print("="*60)
