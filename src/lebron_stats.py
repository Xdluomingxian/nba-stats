#!/usr/bin/env python3
"""
勒布朗·詹姆斯职业生涯数据统计
获取生涯总得分、篮板、助攻等数据以及最近比赛表现
"""
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from nba_api.stats.endpoints import playercareerstats, playergamelog
from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.static import players
import pandas as pd


def get_player_id(player_name: str) -> str:
    """
    根据球员姓名获取 player_id
    
    Args:
        player_name: 球员姓名
        
    Returns:
        player_id 字符串
    """
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict:
        return player_dict[0]['id']
    return None


def get_career_stats(player_id: str) -> dict:
    """
    获取球员生涯统计数据
    
    Args:
        player_id: 球员 ID
        
    Returns:
        生涯统计数据字典
    """
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    
    # 常规赛总计
    regular_season = career.season_totals_regular_season.get_data_frame()
    
    # 季后赛总计
    playoff_season = career.season_totals_post_season.get_data_frame()
    
    # 计算生涯总计
    career_totals = {
        'seasons_played': len(regular_season),
        'regular_season': {
            'games': int(regular_season['GP'].sum()),
            'points': int(regular_season['PTS'].sum()),
            'rebounds': int(regular_season['REB'].sum()),
            'assists': int(regular_season['AST'].sum()),
            'steals': int(regular_season['STL'].sum()),
            'blocks': int(regular_season['BLK'].sum()),
            'turnovers': int(regular_season['TOV'].sum()),
            'fg_pct': float(regular_season['FG_PCT'].mean()),
            'fg3_pct': float(regular_season['FG3_PCT'].mean()),
            'ft_pct': float(regular_season['FT_PCT'].mean()),
            'ppg': float(regular_season['PTS'].mean()),
            'rpg': float(regular_season['REB'].mean()),
            'apg': float(regular_season['AST'].mean()),
        },
        'playoffs': {
            'games': int(playoff_season['GP'].sum()) if len(playoff_season) > 0 else 0,
            'points': int(playoff_season['PTS'].sum()) if len(playoff_season) > 0 else 0,
            'rebounds': int(playoff_season['REB'].sum()) if len(playoff_season) > 0 else 0,
            'assists': int(playoff_season['AST'].sum()) if len(playoff_season) > 0 else 0,
        }
    }
    
    return career_totals


def get_recent_games(player_id: str, num_games: int = 10) -> list:
    """
    获取球员最近比赛数据
    
    Args:
        player_id: 球员 ID
        num_games: 比赛场次数
        
    Returns:
        比赛数据列表
    """
    # 获取最近赛季
    current_season = "2025-26"
    
    try:
        game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=current_season,
            season_type_all_star=['Regular Season']
        )
        
        # 使用 get_dict 然后转换为 DataFrame
        data = game_log.get_dict()
        if 'resultSets' in data and len(data['resultSets']) > 0:
            df = pd.DataFrame(data['resultSets'][0]['rowSet'], 
                            columns=data['resultSets'][0]['headers'])
            
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


def get_today_games():
    """获取今日比赛"""
    try:
        games = scoreboard.ScoreBoard()
        return games.get_dict()
    except:
        return None


def print_career_stats(stats: dict, player_name: str):
    """打印生涯统计数据"""
    print("="*70)
    print(f"🏀 {player_name} 职业生涯统计数据")
    print("="*70)
    print(f"数据更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 基本信息
    print("【基本信息】")
    print(f"  效力赛季数：{stats['seasons_played']} 个赛季")
    print()
    
    # 常规赛数据
    rs = stats['regular_season']
    print("【常规赛总计】")
    print(f"  出场次数：   {rs['games']:,} 场")
    print(f"  总得分：     {rs['points']:,} 分")
    print(f"  总篮板：     {rs['rebounds']:,} 个")
    print(f"  总助攻：     {rs['assists']:,} 次")
    print(f"  总抢断：     {rs['steals']:,} 次")
    print(f"  总盖帽：     {rs['blocks']:,} 次")
    print(f"  总失误：     {rs['turnovers']:,} 次")
    print()
    
    print("【常规赛场均】")
    print(f"  得分：       {rs['ppg']:.1f} 分")
    print(f"  篮板：       {rs['rpg']:.1f} 个")
    print(f"  助攻：       {rs['apg']:.1f} 次")
    print(f"  投篮命中率： {rs['fg_pct']*100:.1f}%")
    print(f"  三分命中率： {rs['fg3_pct']*100:.1f}%")
    print(f"  罚球命中率： {rs['ft_pct']*100:.1f}%")
    print()
    
    # 季后赛数据
    po = stats['playoffs']
    print("【季后赛总计】")
    print(f"  出场次数：   {po['games']:,} 场")
    print(f"  总得分：     {po['points']:,} 分")
    print(f"  总篮板：     {po['rebounds']:,} 个")
    print(f"  总助攻：     {po['assists']:,} 次")
    print()
    
    # 历史排名
    print("【NBA 历史排名】")
    print(f"  总得分：     历史第 1 位 👑")
    print(f"  总助攻：     历史前 5 位")
    print(f"  总篮板：     历史前 10 位")
    print()


def print_recent_games(games: list, player_name: str):
    """打印最近比赛数据"""
    if not games:
        print("【最近比赛】")
        print("  暂无比赛数据")
        print()
        return
    
    print("="*70)
    print(f"📊 {player_name} 最近比赛数据")
    print("="*70)
    print()
    
    # 计算最近场均
    avg_points = sum(g['points'] for g in games) / len(games)
    avg_rebounds = sum(g['rebounds'] for g in games) / len(games)
    avg_assists = sum(g['assists'] for g in games) / len(games)
    
    print(f"【最近 {len(games)} 场场均】")
    print(f"  得分：  {avg_points:.1f} 分")
    print(f"  篮板：  {avg_rebounds:.1f} 个")
    print(f"  助攻：  {avg_assists:.1f} 次")
    print()
    
    print("【比赛详情】")
    for i, game in enumerate(games[:5], 1):
        date = game['date'].strftime('%m-%d') if hasattr(game['date'], 'strftime') else str(game['date'])[:10]
        print(f"  {i}. {date} {game['matchup']}")
        print(f"     结果：{game['result']} | 得分：{game['points']} | 篮板：{game['rebounds']} | 助攻：{game['assists']}")
        print(f"     投篮：{game['fg_pct']*100:.1f}% | 三分：{game['fg3_pct']*100:.1f}% | 罚球：{game['ft_pct']*100:.1f}%")
        print()


def save_to_csv(stats: dict, games: list, player_name: str):
    """保存数据到 CSV 文件"""
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # 保存生涯数据
    career_file = data_dir / f'{player_name.replace(" ", "_")}_career_stats.csv'
    
    career_data = {
        '类别': ['常规赛总得分', '常规赛总篮板', '常规赛总助攻', '常规赛总抢断', '常规赛总盖帽',
                '常规赛场均得分', '常规赛场均篮板', '常规赛场均助攻',
                '季后赛总得分', '季后赛总篮板', '季后赛总助攻'],
        '数值': [
            stats['regular_season']['points'],
            stats['regular_season']['rebounds'],
            stats['regular_season']['assists'],
            stats['regular_season']['steals'],
            stats['regular_season']['blocks'],
            stats['regular_season']['ppg'],
            stats['regular_season']['rpg'],
            stats['regular_season']['apg'],
            stats['playoffs']['points'],
            stats['playoffs']['rebounds'],
            stats['playoffs']['assists']
        ]
    }
    
    df_career = pd.DataFrame(career_data)
    df_career.to_csv(career_file, index=False, encoding='utf-8-sig')
    print(f"✅ 生涯数据已保存：{career_file}")
    
    # 保存比赛数据
    if games:
        games_file = data_dir / f'{player_name.replace(" ", "_")}_recent_games.csv'
        df_games = pd.DataFrame(games)
        df_games.to_csv(games_file, index=False, encoding='utf-8-sig')
        print(f"✅ 比赛数据已保存：{games_file}")


def main():
    """主函数"""
    player_name = "LeBron James"
    
    print()
    print("="*70)
    print("🏀 NBA 球员数据统计 - LeBron James")
    print("="*70)
    print()
    
    # 获取球员 ID
    print("正在获取球员信息...")
    player_id = get_player_id(player_name)
    
    if not player_id:
        print(f"❌ 未找到球员：{player_name}")
        return
    
    print(f"✅ 找到球员：{player_name} (ID: {player_id})")
    print()
    
    # 获取生涯数据
    print("正在获取生涯统计数据...")
    career_stats = get_career_stats(player_id)
    
    if career_stats:
        print("✅ 生涯数据获取成功")
        print()
        print_career_stats(career_stats, player_name)
    else:
        print("❌ 生涯数据获取失败")
        return
    
    # 获取最近比赛
    print("正在获取最近比赛数据...")
    recent_games = get_recent_games(player_id, num_games=10)
    
    if recent_games:
        print(f"✅ 获取到 {len(recent_games)} 场比赛数据")
        print()
        print_recent_games(recent_games, player_name)
    else:
        print("⚠️ 最近比赛数据获取失败（可能赛季未开始）")
        print()
    
    # 保存数据
    print("正在保存数据...")
    save_to_csv(career_stats, recent_games, player_name)
    
    print()
    print("="*70)
    print("✅ 数据获取完成！")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
