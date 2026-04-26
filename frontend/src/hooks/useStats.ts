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
const REFRESH_INTERVAL = 2 * 60 * 1000; // 2分钟自动刷新一次
const FORCE_REFRESH_ON_FOCUS = true; // 页面获得焦点时强制刷新
const MAX_CACHE_AGE = 60 * 1000; // 本地缓存最大有效期1分钟

// 赛季类型
export type SeasonType = 'Regular Season' | 'Playoffs';

interface UseStatsReturn {
  todayGame: TodayGameStats | null;
  careerStats: CareerStats | null;
  playoffCareerStats: CareerStats | null; // 季后赛生涯数据
  rankings: RankingData[];
  loading: boolean;
  error: string | null;
  refetch: (force?: boolean) => void;
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

// 从本地存储加载缓存
const loadLocalCache = (): DataCache | null => {
  try {
    const cached = localStorage.getItem('lebron_stats_cache');
    if (cached) {
      const parsed = JSON.parse(cached);
      // 检查缓存是否过期
      if (Date.now() - parsed.timestamp < MAX_CACHE_AGE) {
        return parsed;
      }
    }
  } catch (e) {
    console.log('[useStats] 本地缓存加载失败');
  }
  return null;
};

// 保存到本地存储
const saveLocalCache = (data: DataCache) => {
  try {
    localStorage.setItem('lebron_stats_cache', JSON.stringify(data));
  } catch (e) {
    console.log('[useStats] 本地缓存保存失败');
  }
};

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

  // 使用ref跟踪是否已经加载过初始数据
  const initialLoadDone = useRef(false);
  // 跟踪最近一次成功获取的数据，用于对比
  const lastDataRef = useRef<DataCache | null>(null);
  // 用ref缓存当前状态值，避免useCallback依赖变化导致无限循环
  const todayGameRef = useRef<TodayGameStats | null>(null);
  // 跟踪当前赛季类型
  const seasonTypeRef = useRef<SeasonType>('Regular Season');

  const fetchData = useCallback(
    async (force: boolean = false) => {
      const currentSeasonType = seasonTypeRef.current;
      
      // 如果不是强制刷新，先检查本地缓存
      if (!force && !USE_MOCK) {
        const localCache = loadLocalCache();
        if (localCache) {
          console.log('[useStats] 使用本地缓存数据');
          setTodayGame(localCache.todayGame);
          setCareerStats(localCache.careerStats);
          setRankings(localCache.rankings);
          setLastUpdated(new Date(localCache.timestamp));

          // 如果已经加载过初始数据，不再显示loading
          if (initialLoadDone.current) {
            setLoading(false);
          }
        }
      }

      setLoading(true);
      setError(null);

      try {
        if (USE_MOCK) {
          // 使用Mock API获取数据
          const { todayGame: game, career } = await mockApi.fetchAllStats();
          setTodayGame(game);
          setCareerStats(career.stats);
          setRankings(career.rankings);
          setLastUpdated(new Date());
        } else {
          // 使用真实API - 添加时间戳防止浏览器缓存
          const timestamp = Date.now();
          const cacheParam = force ? `&_force=${timestamp}` : `&_t=${timestamp}`;

          console.log(`[useStats] 从服务器获取数据${force ? ' (强制刷新)' : ''}...`);

          // 获取战报数据（带赛季类型）
          const gameRes = await fetch(
            `${API_BASE_URL}/today-game?season_type=${encodeURIComponent(currentSeasonType)}&${cacheParam}`,
            {
              cache: 'no-store',
              headers: {
                'Cache-Control': 'no-cache',
                Pragma: 'no-cache',
              },
            }
          );

          // 并行获取生涯数据和季后赛数据
          const [careerRes, playoffRes] = await Promise.all([
            fetch(`${API_BASE_URL}/career-stats?${cacheParam}`, {
              cache: 'no-store',
              headers: {
                'Cache-Control': 'no-cache',
                Pragma: 'no-cache',
              },
            }),
            fetch(`${API_BASE_URL}/playoff-career-stats?${cacheParam}`, {
              cache: 'no-store',
              headers: {
                'Cache-Control': 'no-cache',
                Pragma: 'no-cache',
              },
            }),
          ]);

          if (!gameRes.ok) throw new Error('获取战报数据失败');
          if (!careerRes.ok) throw new Error('获取生涯数据失败');

          const gameData = await gameRes.json();
          const careerData = await careerRes.json();
          const playoffData = await playoffRes.json();

          // 处理后端返回的 {game: null} 格式
          const actualGameData = gameData.game !== undefined ? gameData.game : gameData;

          // 数据校验：对比新数据和旧数据
          const newData: DataCache = {
            todayGame: actualGameData,
            careerStats: careerData.stats,
            rankings: careerData.rankings,
            timestamp: Date.now(),
          };

          // 检查数据是否有变化
          if (lastDataRef.current) {
            const oldData = lastDataRef.current;
            const hasChanges =
              JSON.stringify(oldData.todayGame) !== JSON.stringify(newData.todayGame) ||
              JSON.stringify(oldData.careerStats) !== JSON.stringify(newData.careerStats);

            if (hasChanges) {
              console.log('[useStats] 检测到数据变化，更新显示');
            } else {
              console.log('[useStats] 数据无变化');
            }
          }

          // 更新状态（允许 todayGame 为 null）
          setTodayGame(actualGameData);
          setCareerStats(careerData.stats);
          setRankings(careerData.rankings);
          
          // 更新季后赛数据
          if (playoffData && playoffData.stats) {
            setPlayoffCareerStats(playoffData.stats);
          }
          
          setLastUpdated(new Date());

          // 保存到本地缓存
          saveLocalCache(newData);
          lastDataRef.current = newData;
        }

        initialLoadDone.current = true;
      } catch (err) {
        console.error('[useStats] 获取数据失败:', err);
        setError(err instanceof Error ? err.message : '未知错误');

        // 如果获取失败但有本地缓存，使用缓存数据
        const localCache = loadLocalCache();
        if (localCache && !todayGameRef.current) {
          console.log('[useStats] 使用本地缓存作为回退');
          setTodayGame(localCache.todayGame);
          setCareerStats(localCache.careerStats);
          setRankings(localCache.rankings);
        }
      } finally {
        setLoading(false);
      }
    },
    [USE_MOCK]
  );

  // 同步ref
  useEffect(() => {
    todayGameRef.current = todayGame;
  }, [todayGame]);

  useEffect(() => {
    seasonTypeRef.current = seasonType;
  }, [seasonType]);

  useEffect(() => {
    // 初始加载和赛季类型变化时刷新数据
    fetchData(true); // 强制刷新以获取最新数据

    // 定时自动刷新（仅真实API模式）
    let interval: NodeJS.Timeout;
    if (!USE_MOCK) {
      interval = setInterval(() => {
        console.log('[useStats] 定时自动刷新');
        fetchData();
      }, REFRESH_INTERVAL);
    }

    // 页面可见性变化监听
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        console.log('[useStats] 页面变为可见，检查数据更新');
        // 检查本地缓存是否过期
        const localCache = loadLocalCache();
        if (!localCache || Date.now() - localCache.timestamp > MAX_CACHE_AGE) {
          console.log('[useStats] 缓存过期，强制刷新');
          fetchData(true);
        }
      }
    };

    // 页面获得焦点时刷新
    const handleFocus = () => {
      if (FORCE_REFRESH_ON_FOCUS && !USE_MOCK) {
        console.log('[useStats] 页面获得焦点，强制刷新数据');
        fetchData(true);
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('focus', handleFocus);

    return () => {
      if (interval) clearInterval(interval);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('focus', handleFocus);
    };
  }, [fetchData]);

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

// 自定义Hook：仅获取今日战报（带校验）
export function useTodayGame() {
  const [data, setData] = useState<TodayGameStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchData = useCallback(async (force: boolean = false) => {
    setLoading(true);
    try {
      if (USE_MOCK) {
        const game = await mockApi.fetchTodayGame();
        setData(game);
      } else {
        const timestamp = Date.now();
        const cacheParam = force ? `&_force=${timestamp}` : `&_t=${timestamp}`;

        const res = await fetch(`${API_BASE_URL}/today-game?${cacheParam}`, {
          cache: 'no-store',
          headers: {
            'Cache-Control': 'no-cache',
            Pragma: 'no-cache',
          },
        });

        if (!res.ok) throw new Error('获取今日战报失败');

        const json = await res.json();
        setData(json);
        setLastUpdated(new Date());

        console.log('[useTodayGame] 数据已更新:', json.date);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData, lastUpdated };
}

// 自定义Hook：仅获取生涯数据（带校验）
export function useCareerStats() {
  const [stats, setStats] = useState<CareerStats | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchData = useCallback(async (force: boolean = false) => {
    setLoading(true);
    try {
      if (USE_MOCK) {
        const data = await mockApi.fetchCareerStats();
        setStats(data.stats);
        setRankings(data.rankings);
      } else {
        const timestamp = Date.now();
        const cacheParam = force ? `&_force=${timestamp}` : `&_t=${timestamp}`;

        const res = await fetch(`${API_BASE_URL}/career-stats?${cacheParam}`, {
          cache: 'no-store',
          headers: {
            'Cache-Control': 'no-cache',
            Pragma: 'no-cache',
          },
        });

        if (!res.ok) throw new Error('获取生涯数据失败');

        const json = await res.json();
        setStats(json.stats);
        setRankings(json.rankings);
        setLastUpdated(new Date());

        console.log('[useCareerStats] 数据已更新');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { stats, rankings, loading, error, refetch: fetchData, lastUpdated };
}
