"""
NBA 数据 API 服务 - LeBron James 数据展示后端
提供詹姆斯比赛数据、生涯统计和历史排名的 API 接口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from datetime import datetime
import sys
import os
import logging
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from nba_data_client import NBADataClient

# 配置日志
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 应用
app = FastAPI(
    title="NBA Stats API - LeBron James",
    description="勒布朗·詹姆斯职业生涯数据展示 API",
    version="1.0.0"
)

# 配置 CORS（生产环境从环境变量读取）
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", 
    "http://localhost:5173,http://127.0.0.1:5173,http://10.3.0.14:5173"
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
        "version": "1.0.0",
        "endpoints": [
            "/api/today-game",
            "/api/career-stats",
            "/api/all-stats"
        ]
    }


@app.get("/api/today-game")
async def get_today_game():
    """
    获取詹姆斯最近一场比赛数据
    
    返回最近一场比赛的详细统计，包括得分、篮板、助攻等数据
    """
    try:
        game_data = client.get_lebron_recent_game()
        
        if not game_data:
            return JSONResponse(
                status_code=204,
                content={"message": "No game data available"}
            )
        
        return game_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch game data: {str(e)}"
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
        
        return {
            "stats": career_stats,
            "rankings": rankings
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch career stats: {str(e)}"
        )


@app.get("/api/all-stats")
async def get_all_stats():
    """
    批量获取所有数据
    
    一次性获取今日战报和生涯数据，减少前端请求次数
    """
    try:
        # 并行获取数据
        game_data = client.get_lebron_recent_game()
        career_stats = client.get_lebron_career_stats()
        rankings = client.get_historical_rankings(career_stats)
        
        return {
            "todayGame": game_data,
            "career": {
                "stats": career_stats,
                "rankings": rankings
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch all stats: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0"
    }


# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP 错误：{exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"服务器错误：{str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc)
            }
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
