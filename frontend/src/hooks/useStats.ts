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
  playoffCareerStats: CareerStats | null;
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
        saveLocalCache({
          todayGame: game,
          careerStats: career.stats,
          rankings: career.rankings,
          timestamp: Date.now(),
        });
      } else {
        const currentSeasonType = seasonTypeRef.current;
        const timestamp = Date.now();
        const cacheParam = `_t=${timestamp}`;

        console.log(`[useStats] 获取数据 (赛季: ${currentSeasonType})...`);

        // 使用批量接口，一次请求获取所有数据
        const allRes = await safeFetch(
          `${API_BASE_URL}/all-stats?season_type=${encodeURIComponent(currentSeasonType)}&${cacheParam}`
        );
        if (allRes && allRes.ok) {
          try {
            const data = await allRes.json();
            const gameData = data.todayGame?.game !== undefined ? data.todayGame.game : data.todayGame;
            setTodayGame(gameData);
            if (data.career?.stats) {
              setCareerStats(data.career.stats);
            }
            if (data.career?.rankings) {
              setRankings(data.career.rankings);
            }
            if (data.playoffCareer?.stats) {
              setPlayoffCareerStats(data.playoffCareer.stats);
            }
            setLastUpdated(new Date());
            saveLocalCache({
              todayGame: gameData,
              careerStats: data.career?.stats || null,
              playoffCareerStats: data.playoffCareer?.stats || null,
              rankings: data.career?.rankings || [],
              timestamp: Date.now(),
            });
          } catch (e) {
            console.error('[useStats] 解析数据失败', e);
          }
        } else {
          console.warn('[useStats] all-stats API 不可用');
        }
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
