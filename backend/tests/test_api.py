"""
API 接口测试
使用 pytest + httpx 测试 FastAPI 接口
"""

import pytest
from httpx import ASGITransport, AsyncClient

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, __version__


@pytest.fixture
async def client():
    """创建异步测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
class TestHealthEndpoint:
    """健康检查接口测试"""

    async def test_health_check(self, client):
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["api_version"] == __version__
        assert "timestamp" in data


@pytest.mark.asyncio
class TestRootEndpoint:
    """根路径接口测试"""

    async def test_root(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == __version__
        assert "/api/today-game" in data["endpoints"]


@pytest.mark.asyncio
class TestCORSHeaders:
    """CORS 响应头测试"""

    async def test_cors_headers(self, client):
        response = await client.options(
            "/api/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
