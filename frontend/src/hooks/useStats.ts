import { useState, useEffect, useCallback, useRef } from 'react';
import type { TodayGameStats, CareerStats, RankingData } from '../data/stats';
import { mockApi } from '../mock/mockApi';

const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  return '/api';
};

const API_BASE_URL = getApiBaseUrl();

// 是否使用Mock数据（通过环境变量控制）
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

// 数据校验配置
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5分钟自动刷新一次
const MAX_CACHE_AGE = 60 * 1000; // 本地缓存最大有效期1分钟

// 赛季类型
export type SeasonType = 'Regular Season' | 'Playoffs';

interface UseStatsReturn {
  todayGame: TodayGameStats | null;
  careerStats: CareerStats | null;
  playoffCareerStats: CareerStats | null;
  rankings: RankingData[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
  lastUpdated: Date | null;
  isMock: boolean;
  seasonType: SeasonType;
  setSeasonType: (type: SeasonType) => void;
}

// 本地存储的数据缓存
interface DataCache {
  todayGame: TodayGameStats | null;
  careerStats: CareerStats | null;
  rankings: RankingData[];
  timestamp: number;
}

const loadLocalCache = (): DataCache | null => {
  try {
    const cached = localStorage.getItem('lebron_stats_cache');
    if (cached) {
      const parsed = JSON.parse(cached);
      if (Date.now() - parsed.timestamp < MAX_CACHE_AGE) {
        return parsed;
      }
    }
  } catch (e) {
    // ignore
  }
  return null;
};

const saveLocalCache = (data: DataCache) => {
  try {
    localStorage.setItem('lebron_stats_cache', JSON.stringify(data));
  } catch (e) {
    // ignore
  }
};

// 安全的 fetch 封装
async function safeFetch(url: string): Promise<Response | null> {
  try {
    const res = await fetch(url, {
      cache: 'no-store',
      headers: { 'Cache-Control': 'no-cache', Pragma: 'no-cache' },
    });
    return res;
  } catch (e) {
    console.error(`[useStats] 请求失败: ${url}`, e);
    return null;
  }
}

// 自定义Hook：获取所有统计数据
export function useStats(): UseStatsReturn {
  const [seasonType, setSeasonType] = useState<SeasonType>('Regular Season');
  const [todayGame, setTodayGame] = useState<TodayGameStats | null>(null);
  const [careerStats, setCareerStats] = useState<CareerStats | null>(null);
  const [playoffCareerStats, setPlayoffCareerStats] = useState<CareerStats | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const seasonTypeRef = useRef<SeasonType>('Regular Season');

  useEffect(() => {
    seasonTypeRef.current = seasonType;
  }, [seasonType]);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      if (USE_MOCK) {
        const { todayGame: game, career } = await mockApi.fetchAllStats();
        setTodayGame(game);
        setCareerStats(career.stats);
        setRankings(career.rankings);
        setLastUpdated(new Date());
      } else {
        const currentSeasonType = seasonTypeRef.current;
        const timestamp = Date.now();
        const cacheParam = `_t=${timestamp}`;

        console.log(`[useStats] 获取数据 (赛季: ${currentSeasonType})...`);

        // 独立请求，互不影响
        // 1. 获取战报数据
        const gameRes = await safeFetch(
          `${API_BASE_URL}/today-game?season_type=${encodeURIComponent(currentSeasonType)}&${cacheParam}`
        );
        if (gameRes && gameRes.ok) {
          try {
            const gameData = await gameRes.json();
            const actualGameData = gameData.game !== undefined ? gameData.game : gameData;
            setTodayGame(actualGameData);
          } catch (e) {
            console.error('[useStats] 解析战报数据失败', e);
            setTodayGame(null);
          }
        } else {
          console.warn('[useStats] 战报API不可用');
          setTodayGame(null);
        }

        // 2. 获取生涯数据
        const careerRes = await safeFetch(`${API_BASE_URL}/career-stats?${cacheParam}`);
        if (careerRes && careerRes.ok) {
          try {
            const careerData = await careerRes.json();
            if (careerData.stats) {
              setCareerStats(careerData.stats);
            }
            if (careerData.rankings) {
              setRankings(careerData.rankings);
            }
          } catch (e) {
            console.error('[useStats] 解析生涯数据失败', e);
          }
        } else {
          console.warn('[useStats] 生涯数据API不可用');
        }

        // 3. 获取季后赛数据
        const playoffRes = await safeFetch(`${API_BASE_URL}/playoff-career-stats?${cacheParam}`);
        if (playoffRes && playoffRes.ok) {
          try {
            const playoffData = await playoffRes.json();
            if (playoffData.stats) {
              setPlayoffCareerStats(playoffData.stats);
            }
          } catch (e) {
            console.error('[useStats] 解析季后赛数据失败', e);
          }
        } else {
          console.warn('[useStats] 季后赛数据API不可用');
        }

        setLastUpdated(new Date());

        // 保存缓存
        // Note: 这里用当前state值，在async中可能不是最新的，但足够用了
      }
    } catch (err) {
      console.error('[useStats] 获取数据失败:', err);
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setLoading(false);
    }
  }, [USE_MOCK]);

  useEffect(() => {
    fetchData();

    let interval: NodeJS.Timeout;
    if (!USE_MOCK) {
      interval = setInterval(() => {
        fetchData();
      }, REFRESH_INTERVAL);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [fetchData, seasonType]);

  return {
    todayGame,
    careerStats,
    playoffCareerStats,
    rankings,
    loading,
    error,
    refetch: fetchData,
    lastUpdated,
    isMock: USE_MOCK,
    seasonType,
    setSeasonType,
  };
}
