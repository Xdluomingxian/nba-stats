// NBA数据API服务层
import type { TodayGameStats, CareerStats, RankingData } from '../data/stats';

const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  return '/api';
};

const API_BASE_URL = getApiBaseUrl();

/**
 * 获取最近一场战报数据
 * GET /api/today-game?season_type=Regular Season|Playoffs
 * Response: TodayGameStats | { game: null, message: string }
 */
export async function fetchRecentGame(seasonType: string = 'Regular Season'): Promise<any> {
  const response = await fetch(
    `${API_BASE_URL}/today-game?season_type=${encodeURIComponent(seasonType)}`
  );
  if (!response.ok) {
    throw new Error('Failed to fetch recent game data');
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
 * 获取季后赛生涯数据
 * GET /api/playoff-career-stats
 * Response: { stats: CareerStats }
 */
export async function fetchPlayoffCareerStats(): Promise<{
  stats: CareerStats;
}> {
  const response = await fetch(`${API_BASE_URL}/playoff-career-stats`);
  if (!response.ok) {
    throw new Error('Failed to fetch playoff career stats');
  }
  return response.json();
}

/**
 * 获取所有数据（战报 + 生涯）
 * GET /api/all-stats
 */
export async function fetchAllStats(seasonType: string = 'Regular Season'): Promise<{
  todayGame: any;
  career: { stats: CareerStats; rankings: RankingData[] };
  playoff?: { stats: CareerStats };
}> {
  const response = await fetch(
    `${API_BASE_URL}/all-stats?season_type=${encodeURIComponent(seasonType)}`
  );
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
