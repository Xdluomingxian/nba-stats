import { useState, useEffect } from 'react';
import type { TodayGameStats, CareerStats, RankingData } from '../data/stats';
import { mockApi } from '../mock/mockApi';

// API基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

// 是否使用Mock数据（通过环境变量控制）
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

interface UseStatsReturn {
  todayGame: TodayGameStats | null;
  careerStats: CareerStats | null;
  rankings: RankingData[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
  isMock: boolean;
}

// 自定义Hook：获取所有统计数据
// 根据 VITE_USE_MOCK 环境变量自动切换 Mock/真实API
export function useStats(): UseStatsReturn {
  const [todayGame, setTodayGame] = useState<TodayGameStats | null>(null);
  const [careerStats, setCareerStats] = useState<CareerStats | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      if (USE_MOCK) {
        // 使用Mock API获取数据
        const { todayGame: game, career } = await mockApi.fetchAllStats();
        setTodayGame(game);
        setCareerStats(career.stats);
        setRankings(career.rankings);
      } else {
        // 使用真实API
        const [todayRes, careerRes] = await Promise.all([
          fetch(`${API_BASE_URL}/today-game`),
          fetch(`${API_BASE_URL}/career-stats`)
        ]);

        if (!todayRes.ok) throw new Error('Failed to fetch today game data');
        if (!careerRes.ok) throw new Error('Failed to fetch career stats');

        const todayData = await todayRes.json();
        const careerData = await careerRes.json();

        setTodayGame(todayData);
        setCareerStats(careerData.stats);
        setRankings(careerData.rankings);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // 每5分钟自动刷新一次（仅真实API模式）
    if (!USE_MOCK) {
      const interval = setInterval(fetchData, 5 * 60 * 1000);
      return () => clearInterval(interval);
    }
  }, []);

  return {
    todayGame,
    careerStats,
    rankings,
    loading,
    error,
    refetch: fetchData,
    isMock: USE_MOCK
  };
}

// 自定义Hook：仅获取今日战报
export function useTodayGame() {
  const [data, setData] = useState<TodayGameStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (USE_MOCK) {
        const game = await mockApi.fetchTodayGame();
        setData(game);
      } else {
        const res = await fetch(`${API_BASE_URL}/today-game`);
        if (!res.ok) throw new Error('Failed to fetch');
        const json = await res.json();
        setData(json);
      }
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

// 自定义Hook：仅获取生涯数据
export function useCareerStats() {
  const [stats, setStats] = useState<CareerStats | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (USE_MOCK) {
        const data = await mockApi.fetchCareerStats();
        setStats(data.stats);
        setRankings(data.rankings);
      } else {
        const res = await fetch(`${API_BASE_URL}/career-stats`);
        if (!res.ok) throw new Error('Failed to fetch');
        const json = await res.json();
        setStats(json.stats);
        setRankings(json.rankings);
      }
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
