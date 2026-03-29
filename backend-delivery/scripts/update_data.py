#!/usr/bin/env python3
"""
NBA 数据更新脚本
定期更新詹姆斯比赛数据和生涯统计
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nba_data_client import NBADataClient


def update_data():
    """更新詹姆斯数据"""
    client = NBADataClient()
    
    print("=" * 60)
    print("🏀 NBA 数据更新")
    print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 获取最新数据
    print("\n【1. 获取最近比赛数据】")
    recent_game = client.get_lebron_recent_game()
    if recent_game:
        print(f"✅ 对手：{recent_game['opponent']}, 日期：{recent_game['date']}")
        print(f"   数据：{recent_game['points']}分 {recent_game['rebounds']}板 {recent_game['assists']}助")
    else:
        print("⚠️ 无比赛数据")
    
    print("\n【2. 获取生涯统计数据】")
    career_stats = client.get_lebron_career_stats()
    print(f"✅ 出场：{career_stats['games']}场")
    print(f"   得分：{career_stats['points']}分")
    print(f"   篮板：{career_stats['rebounds']}个")
    print(f"   助攻：{career_stats['assists']}次")
    
    print("\n【3. 获取历史排名】")
    rankings = client.get_historical_rankings(career_stats)
    for r in rankings:
        status = "🥇" if r['rank'] == 1 else "📈" if r['gapToPrev'] > 0 else "📊"
        print(f"   {status} {r['category']}: 第{r['rank']}名 ({r['careerValue']})")
    
    # 保存到文件
    print("\n【4. 保存数据】")
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # 保存完整数据
    all_data = {
        "updateTime": datetime.now().isoformat(),
        "todayGame": recent_game,
        "career": {
            "stats": career_stats,
            "rankings": rankings
        }
    }
    
    data_file = data_dir / "lebron_stats.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存到：{data_file}")
    
    # 保存 CSV 格式（最近比赛）
    if recent_game:
        csv_file = data_dir / "lebron_recent_game.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("opponent,date,result,points,rebounds,assists,steals,blocks,minutes,fgPercent,threePercent,ftPercent\n")
            f.write(f"{recent_game['opponent']},{recent_game['date']},{recent_game['result']},{recent_game['points']},{recent_game['rebounds']},{recent_game['assists']},{recent_game['steals']},{recent_game['blocks']},{recent_game['minutes']},{recent_game['fgPercent']},{recent_game['threePercent']},{recent_game['ftPercent']}\n")
        print(f"✅ CSV 已保存到：{csv_file}")
    
    print("\n✅ 数据更新完成！")
    return all_data


if __name__ == "__main__":
    update_data()
