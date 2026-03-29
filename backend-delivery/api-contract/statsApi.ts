// NBA数据API服务层
import type { TodayGameStats, CareerStats, RankingData } from '../data/stats';

// API基础配置 - 根据环境变量配置baseURL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

/**
 * 获取今日战报数据
 * GET /api/today-game
 * Response: TodayGameStats
 */
export async function fetchTodayGame(): Promise<TodayGameStats> {
  const response = await fetch(`${API_BASE_URL}/today-game`);
  if (!response.ok) {
    throw new Error('Failed to fetch today game data');
  }
  return response.json();
}

/**
 * 获取生涯累计数据
 * GET /api/career-stats
 * Response: { stats: CareerStats, rankings: RankingData[] }
 */
export async function fetchCareerStats(): Promise<{
  stats: CareerStats;
  rankings: RankingData[];
}> {
  const response = await fetch(`${API_BASE_URL}/career-stats`);
  if (!response.ok) {
    throw new Error('Failed to fetch career stats');
  }
  return response.json();
}

/**
 * 获取所有数据（今日战报 + 生涯）
 * GET /api/all-stats
 */
export async function fetchAllStats(): Promise<{
  todayGame: TodayGameStats;
  career: { stats: CareerStats; rankings: RankingData[] };
}> {
  const response = await fetch(`${API_BASE_URL}/all-stats`);
  if (!response.ok) {
    throw new Error('Failed to fetch all stats');
  }
  return response.json();
}

// 带缓存的数据获取（可选）
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000; // 5分钟

export async function fetchWithCache<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data as T;
  }
  const data = await fetcher();
  cache.set(key, { data, timestamp: Date.now() });
  return data;
}
