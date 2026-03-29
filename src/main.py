#!/usr/bin/env python3
"""
NBA 统计数据爬虫 - 主程序
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from nba_client import NBAClient


def print_games(games, title="比赛"):
    """打印比赛列表"""
    if not games:
        print(f"  暂无{title}")
        return
    
    for game in games:
        home = game['home_team']
        visitor = game['visitor_team']
        home_score = game.get('home_team_score', 0)
        visitor_score = game.get('visitor_team_score', 0)
        
        status = game.get('status', '')
        
        print(f"  🏀 {visitor['full_name']} @ {home['full_name']}")
        if home_score and visitor_score:
            print(f"     比分：{visitor_score} - {home_score}")
        if status:
            print(f"     状态：{status}")
        print()


def print_players(players, title="球员"):
    """打印球员列表"""
    if not players:
        print(f"  暂无{title}")
        return
    
    for player in players[:10]:
        print(f"  - {player['first_name']} {player['last_name']} "
              f"({player['position']}) - {player['team']['full_name']}")
    print()


def print_teams(teams):
    """打印球队列表"""
    if not teams:
        print("  暂无球队")
        return
    
    for team in teams:
        print(f"  - {team['full_name']} ({team['abbreviation']})")
    print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='NBA 统计数据爬虫')
    
    parser.add_argument('--today', action='store_true', help='获取今日比赛')
    parser.add_argument('--yesterday', action='store_true', help='获取昨日比赛')
    parser.add_argument('--player', type=str, help='搜索球员')
    parser.add_argument('--team', type=str, help='搜索球队')
    parser.add_argument('--teams', action='store_true', help='获取所有球队')
    parser.add_argument('--schedule', action='store_true', help='获取赛程')
    
    args = parser.parse_args()
    
    # 初始化客户端
    client = NBAClient()
    
    print("="*60)
    print("🏀 NBA 统计数据爬虫")
    print(f"运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()
    
    # 今日比赛
    if args.today:
        print("【今日比赛】")
        games = client.get_today_games()
        print_games(games, "今日比赛")
    
    # 昨日比赛
    if args.yesterday:
        print("【昨日比赛】")
        games = client.get_yesterday_games()
        print_games(games, "昨日比赛")
    
    # 搜索球员
    if args.player:
        print(f"【搜索球员：{args.player}】")
        players = client.search_player(args.player)
        print_players(players, f"{args.player} 相关球员")
    
    # 搜索球队
    if args.team:
        print(f"【搜索球队：{args.team}】")
        team = client.get_team_by_name(args.team)
        if team:
            print(f"  - {team['full_name']} ({team['abbreviation']})")
            print(f"    城市：{team['city']}")
            print(f"    分区：{team['division']} - {team['conference']}")
        else:
            print(f"  未找到球队：{args.team}")
        print()
    
    # 所有球队
    if args.teams:
        print("【NBA 球队列表】")
        teams = client.get_teams()
        print_teams(teams)
    
    # 赛程
    if args.schedule:
        print("【近期赛程】")
        games = client.get_today_games()
        print_games(games, "赛程")
    
    # 默认显示帮助
    if len(sys.argv) == 1:
        parser.print_help()


if __name__ == "__main__":
    main()
