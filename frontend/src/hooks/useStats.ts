import { useState, useEffect } from 'react';
import type { TodayGameStats, CareerStats, RankingData } from '../types/stats';
import { fetchAllStats, checkHealth } from '../api/statsApi';

interface UseStatsReturn {
  todayGame: TodayGameStats | null;
  careerStats: CareerStats | null;
  rankings: RankingData[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
  apiHealthy: boolean;
}

/**
 * 自定义 Hook：获取所有统计数据
 */
export function useStats(): UseStatsReturn {
  const [todayGame, setTodayGame] = useState<TodayGameStats | null>(null);
  const [careerStats, setCareerStats] = useState<CareerStats | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [apiHealthy, setApiHealthy] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // 检查 API 健康状态
      const healthy = await checkHealth();
      setApiHealthy(healthy);
      
      if (!healthy) {
        throw new Error('API 服务不可用，请检查后端是否启动');
      }

      // 使用批量接口获取所有数据
      const data = await fetchAllStats();
      
      setTodayGame(data.todayGame);
      setCareerStats(data.career.stats);
      setRankings(data.career.rankings);
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // 每 5 分钟自动刷新一次
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return {
    todayGame,
    careerStats,
    rankings,
    loading,
    error,
    refetch: fetchData,
    apiHealthy
  };
}
