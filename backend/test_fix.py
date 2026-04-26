"""验证今日战报修复"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from nba_data_client import NBADataClient


def test_season_config():
    """测试赛季配置"""
    print("=" * 50)
    print("测试1: 赛季配置检查")
    print("=" * 50)

    # 读取源代码检查赛季配置
    with open("nba_data_client.py", "r", encoding="utf-8") as f:
        content = f.read()
        if 'season="2025-26"' in content:
            print("✅ 赛季配置已更新为 2025-26")
        elif 'season="2024-25"' in content:
            print("❌ 赛季配置仍为 2024-25，需要修复")
        else:
            print("⚠️ 未找到赛季配置")


def test_data_fetch():
    """测试数据获取"""
    print("\n" + "=" * 50)
    print("测试2: 数据获取测试")
    print("=" * 50)

    client = NBADataClient()
    print(f"使用真实API: {client.use_real_api}")

    try:
        game = client.get_lebron_recent_game()
        if game:
            print(f"✅ 获取到比赛数据:")
            print(f"   对手: {game.get('opponent')}")
            print(f"   日期: {game.get('date')}")
            print(f"   结果: {game.get('result')}")
            print(f"   得分: {game.get('points')}")
        else:
            print("⚠️ 未获取到数据，返回None")
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")


def test_cache_files():
    """测试缓存文件"""
    print("\n" + "=" * 50)
    print("测试3: 缓存文件检查")
    print("=" * 50)

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    cache_files = ["recent_game.json", "cache_meta.json"]

    for filename in cache_files:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            print(f"✅ {filename} 存在")
            # 读取并显示内容
            try:
                import json

                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if filename == "recent_game.json":
                        print(f"   比赛日期: {data.get('date')}")
            except Exception as e:
                print(f"   读取失败: {e}")
        else:
            print(f"⚠️ {filename} 不存在（将在首次请求时创建）")


if __name__ == "__main__":
    test_season_config()
    test_data_fetch()
    test_cache_files()
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
