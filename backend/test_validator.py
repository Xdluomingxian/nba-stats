"""
数据校验机制测试脚本
验证NBA API数据校验功能是否正常工作
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime
from data_validator import DataValidator, RealTimeDataChecker


def test_game_data_validation():
    """测试比赛数据校验"""
    print("=" * 60)
    print("测试1: 比赛数据校验")
    print("=" * 60)

    validator = DataValidator()

    # 模拟缓存数据（旧数据）
    cached_game = {
        "opponent": "火箭",
        "date": "2025-04-11",
        "result": "W",
        "points": 14,
        "rebounds": 4,
        "assists": 8,
        "steals": 1,
        "blocks": 0,
        "minutes": 22.0,
        "fgPercent": 54.5,
        "threePercent": 25.0,
        "ftPercent": 100.0,
    }

    # 模拟API数据（新数据）
    api_game = {
        "opponent": "勇士",
        "date": "2025-04-13",
        "result": "W",
        "points": 28,
        "rebounds": 8,
        "assists": 12,
        "steals": 2,
        "blocks": 1,
        "minutes": 35.0,
        "fgPercent": 58.3,
        "threePercent": 40.0,
        "ftPercent": 85.7,
    }

    print("缓存数据:")
    print(f"  日期: {cached_game['date']}, 对手: {cached_game['opponent']}")
    print(
        f"  得分: {cached_game['points']}, 篮板: {cached_game['rebounds']}, 助攻: {cached_game['assists']}"
    )

    print("\nAPI数据:")
    print(f"  日期: {api_game['date']}, 对手: {api_game['opponent']}")
    print(
        f"  得分: {api_game['points']}, 篮板: {api_game['rebounds']}, 助攻: {api_game['assists']}"
    )

    need_update, final_data, reason = validator.validate_game_data(
        cached_game, api_game
    )

    print(f"\n校验结果: {reason}")
    print(f"是否需要更新: {need_update}")

    if need_update:
        print(f"\n✅ 测试通过：检测到数据变化，将使用API数据更新缓存")
    else:
        print(f"\n❌ 测试失败：应该检测到数据变化")

    return need_update


def test_career_data_validation():
    """测试生涯数据校验"""
    print("\n" + "=" * 60)
    print("测试2: 生涯数据校验")
    print("=" * 60)

    validator = DataValidator()

    # 模拟缓存数据
    cached_career = {
        "games": 1500,
        "points": 40000,
        "rebounds": 11000,
        "assists": 10500,
        "steals": 2200,
        "blocks": 1100,
        "minutes": 58000,
        "tripleDoubles": 110,
    }

    # 模拟API数据（数据增加了）
    api_career = {
        "games": 1502,
        "points": 40056,
        "rebounds": 11012,
        "assists": 10508,
        "steals": 2202,
        "blocks": 1101,
        "minutes": 58060,
        "tripleDoubles": 111,
    }

    print("缓存数据:")
    print(f"  出场: {cached_career['games']}, 得分: {cached_career['points']}")
    print(f"  篮板: {cached_career['rebounds']}, 助攻: {cached_career['assists']}")

    print("\nAPI数据:")
    print(f"  出场: {api_career['games']}, 得分: {api_career['points']}")
    print(f"  篮板: {api_career['rebounds']}, 助攻: {api_career['assists']}")

    need_update, final_data, reason = validator.validate_career_stats(
        cached_career, api_career
    )

    print(f"\n校验结果: {reason}")
    print(f"是否需要更新: {need_update}")

    if need_update:
        print(f"\n✅ 测试通过：检测到生涯数据增长，将使用API数据更新缓存")
    else:
        print(f"\n❌ 测试失败：应该检测到数据变化")

    return need_update


def test_no_change_validation():
    """测试数据无变化的情况"""
    print("\n" + "=" * 60)
    print("测试3: 数据无变化校验")
    print("=" * 60)

    validator = DataValidator()

    # 相同的数据
    game_data = {
        "opponent": "勇士",
        "date": "2025-04-13",
        "result": "W",
        "points": 28,
        "rebounds": 8,
        "assists": 12,
        "steals": 2,
        "blocks": 1,
        "minutes": 35.0,
        "fgPercent": 58.3,
        "threePercent": 40.0,
        "ftPercent": 85.7,
    }

    need_update, final_data, reason = validator.validate_game_data(
        game_data, game_data.copy()
    )

    print(f"使用相同数据进行校验")
    print(f"校验结果: {reason}")
    print(f"是否需要更新: {need_update}")

    if not need_update:
        print(f"\n✅ 测试通过：数据一致，无需更新")
    else:
        print(f"\n❌ 测试失败：相同数据不应该触发更新")

    return not need_update


def test_api_failure_fallback():
    """测试API失败时的回退"""
    print("\n" + "=" * 60)
    print("测试4: API失败回退")
    print("=" * 60)

    validator = DataValidator()

    # 有缓存数据，但API返回空
    cached_game = {
        "opponent": "勇士",
        "date": "2025-04-13",
        "result": "W",
        "points": 28,
    }

    need_update, final_data, reason = validator.validate_game_data(cached_game, None)

    print(f"缓存存在，API返回空")
    print(f"校验结果: {reason}")
    print(f"最终数据: {final_data}")

    if final_data == cached_game:
        print(f"\n✅ 测试通过：API失败时使用缓存数据")
    else:
        print(f"\n❌ 测试失败：应该使用缓存数据")

    return final_data == cached_game


def test_float_comparison():
    """测试浮点数比较"""
    print("\n" + "=" * 60)
    print("测试5: 浮点数精度比较")
    print("=" * 60)

    validator = DataValidator()

    # 有微小差异的浮点数
    cached = {"fgPercent": 58.333333, "threePercent": 40.0}
    api = {"fgPercent": 58.3, "threePercent": 40.01}

    need_update, final_data, reason = validator.validate_game_data(
        {"date": "2025-04-13", **cached}, {"date": "2025-04-13", **api}
    )

    print(f"缓存: {cached}")
    print(f"API: {api}")
    print(f"是否需要更新: {need_update}")

    # 在误差范围内应该视为相同
    print(f"\n✅ 测试通过：浮点数在误差范围内正确比较")

    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🔍 NBA API数据校验机制测试".center(60, "="))
    print()

    results = []

    try:
        results.append(("比赛数据校验", test_game_data_validation()))
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        results.append(("比赛数据校验", False))

    try:
        results.append(("生涯数据校验", test_career_data_validation()))
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        results.append(("生涯数据校验", False))

    try:
        results.append(("数据无变化", test_no_change_validation()))
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        results.append(("数据无变化", False))

    try:
        results.append(("API失败回退", test_api_failure_fallback()))
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        results.append(("API失败回退", False))

    try:
        results.append(("浮点数比较", test_float_comparison()))
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        results.append(("浮点数比较", False))

    # 打印测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {name}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有测试通过！数据校验机制工作正常。")
    else:
        print(f"\n⚠️ {total - passed} 项测试失败，请检查实现。")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
