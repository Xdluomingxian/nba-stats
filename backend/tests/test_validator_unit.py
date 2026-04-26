"""
数据校验模块单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_validator import DataValidator


class TestDataValidator:
    """数据校验器测试"""

    def setup_method(self):
        self.validator = DataValidator()

    def test_validate_game_data_with_changes(self):
        """测试检测到数据变化时触发更新"""
        cached = {"date": "2025-04-11", "points": 14, "rebounds": 4}
        api = {"date": "2025-04-13", "points": 28, "rebounds": 8}

        need_update, final_data, reason = self.validator.validate_game_data(
            cached, api
        )

        assert need_update is True
        assert final_data == api
        assert "变化" in reason or "更新" in reason

    def test_validate_game_data_no_changes(self):
        """测试数据无变化时不触发更新"""
        game = {"date": "2025-04-13", "points": 28, "rebounds": 8}

        need_update, final_data, reason = self.validator.validate_game_data(
            game, game.copy()
        )

        assert need_update is False

    def test_validate_game_data_api_failure_fallback(self):
        """测试 API 失败时回退到缓存"""
        cached = {"date": "2025-04-13", "points": 28}

        need_update, final_data, reason = self.validator.validate_game_data(
            cached, None
        )

        assert final_data == cached
        assert need_update is False

    def test_validate_career_stats_growth(self):
        """测试生涯数据增长检测"""
        cached = {"games": 1500, "points": 40000}
        api = {"games": 1502, "points": 40056}

        need_update, final_data, reason = self.validator.validate_career_stats(
            cached, api
        )

        assert need_update is True
        assert final_data == api
