import { useState, useEffect } from 'react';
import type { TodayGameStats, CareerStats, RankingData } from '../data/stats';
import { mockApi } from '../mock/mockApi';

// 是否使用Mock数据（通过环境变量控制）
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

interface UseMockStatsReturn {
  todayGame: TodayGameStats | null;
  careerStats: CareerStats | null;
  rankings: RankingData[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

// 使用Mock数据的Hook
export function useMockStats(): UseMockStatsReturn {
  const [todayGame, setTodayGame] = useState<TodayGameStats | null>(null);
  const [careerStats, setCareerStats] = useState<CareerStats | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      // 使用Mock API获取数据
      const { todayGame: game, career } = await mockApi.fetchAllStats();

      setTodayGame(game);
      setCareerStats(career.stats);
      setRankings(career.rankings);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (USE_MOCK) {
      fetchData();
    }
  }, []);

  return {
    todayGame,
    careerStats,
    rankings,
    loading,
    error,
    refetch: fetchData,
  };
}

// 仅获取今日战报（Mock版本）
export function useMockTodayGame() {
  const [data, setData] = useState<TodayGameStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const game = await mockApi.fetchTodayGame();
      setData(game);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { data, loading, error, refetch: fetchData };
}

// 仅获取生涯数据（Mock版本）
export function useMockCareerStats() {
  const [stats, setStats] = useState<CareerStats | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await mockApi.fetchCareerStats();
      setStats(data.stats);
      setRankings(data.rankings);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { stats, rankings, loading, error, refetch: fetchData };
}

export default useMockStats;
