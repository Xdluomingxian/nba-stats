"""
NBA 数据 API 服务 - LeBron James 数据展示后端
提供詹姆斯比赛数据、生涯统计和历史排名的 API 接口
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from datetime import datetime
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from nba_data_client import NBADataClient

# 限流（slowapi）
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded

    limiter = Limiter(key_func=get_remote_address)
    RATE_LIMIT_AVAILABLE = True
except ImportError:
    RATE_LIMIT_AVAILABLE = False
    limiter = None

__version__ = "1.4.0"

# 配置日志（支持轮转，单文件最大 10MB，保留 5 个备份）
os.makedirs("logs", exist_ok=True)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("logs/api.log", maxBytes=10 * 1024 * 1024, backupCount=5),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 应用
app = FastAPI(
    title="NBA Stats API - LeBron James",
    description="勒布朗·詹姆斯职业生涯数据展示 API",
    version=__version__,
)

# 注册限流异常处理器
def conditional_limit(limit_string: str):
    """条件限流装饰器：slowapi 可用时启用限流，否则为空装饰器"""
    def decorator(func):
        if RATE_LIMIT_AVAILABLE and limiter:
            return limiter.limit(limit_string)(func)
        return func
    return decorator

if RATE_LIMIT_AVAILABLE and limiter:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("API rate limiting enabled")
else:
    logger.info("WARNING: slowapi not installed, rate limiting disabled")

# 配置 CORS（生产环境从环境变量读取）
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# 初始化数据客户端
client = NBADataClient()


@app.get("/")
async def root():
    """API 根路径"""
    return {
        "message": "NBA Stats API - LeBron James",
        "version": __version__,
        "endpoints": ["/api/today-game", "/api/career-stats", "/api/all-stats"],
    }


@app.get("/api/today-game")
@conditional_limit("30/minute")
async def get_today_game(request: Request, season_type: str = "Regular Season"):
    """
    获取詹姆斯最近一场比赛数据

    返回最近一场比赛的详细统计，包括得分、篮板、助攻等数据
    支持时区转换（根据客户端IP）
    如果无比赛数据，返回 null
    
    Args:
        season_type: 赛季类型（Regular Season / Playoffs）
    """
    try:
        # 获取客户端IP
        client_ip = request.client.host if request.client else None

        game_data = client.get_lebron_recent_game(client_ip, season_type=season_type)

        if not game_data:
            # 返回 null 而非 204，让前端处理无数据的情况
            season_label = "季后赛" if season_type == "Playoffs" else "常规赛"
            return {"game": None, "message": f"{season_label}暂无比赛"}

        return game_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch game data: {str(e)}"
        )


@app.get("/api/playoff-career-stats")
@conditional_limit("30/minute")
async def get_playoff_career_stats(request: Request):
    """
    获取詹姆斯季后赛生涯统计数据
    """
    try:
        playoff_stats = client.get_lebron_playoff_career_stats()
        
        if not playoff_stats:
            return {"stats": {}, "message": "季后赛数据暂无"}
        
        return {"stats": playoff_stats}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch playoff career stats: {str(e)}"
        )


@app.get("/api/career-stats")
async def get_career_stats():
    """
    获取詹姆斯生涯统计数据

    返回职业生涯累计数据及历史排名
    """
    try:
        # 获取生涯数据
        career_stats = client.get_lebron_career_stats()

        # 获取历史排名
        rankings = client.get_historical_rankings(career_stats)

        return {"stats": career_stats, "rankings": rankings}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch career stats: {str(e)}"
        )


@app.get("/api/all-stats")
async def get_all_stats(request: Request, season_type: str = "Regular Season"):
    """
    批量获取所有数据

    一次性获取今日战报、常规赛/季后赛生涯数据和历史排名，减少前端请求次数
    支持时区转换（根据客户端IP）

    Args:
        season_type: 赛季类型（Regular Season / Playoffs）
    """
    try:
        client_ip = request.client.host if request.client else None

        game_data = client.get_lebron_recent_game(client_ip, season_type=season_type)
        career_stats = client.get_lebron_career_stats()
        rankings = client.get_historical_rankings(career_stats)
        playoff_stats = client.get_lebron_playoff_career_stats()

        return {
            "todayGame": game_data,
            "career": {"stats": career_stats, "rankings": rankings},
            "playoffCareer": {"stats": playoff_stats} if playoff_stats else None,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch all stats: {str(e)}"
        )


@app.get("/api/health")
@conditional_limit("60/minute")
async def health_check(request: Request):
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_version": __version__,
    }


# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP 错误：{exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": f"HTTP_{exc.status_code}", "message": exc.detail}},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"服务器错误：{str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_SERVER_ERROR", "message": str(exc)}},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
