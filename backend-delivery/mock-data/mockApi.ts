// Mock API 服务
// 用于本地开发和前端预览，模拟后端API响应

import type { TodayGameStats, CareerStats, RankingData } from '../data/stats';
import { mockTodayGame, mockCareerStats, mockRankings } from './mockData';

// 模拟延迟（毫秒）
const MOCK_DELAY = 500;

// 模拟网络延迟
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Mock API: 获取今日战报
 * GET /api/today-game
 */
export async function mockFetchTodayGame(): Promise<TodayGameStats> {
  await delay(MOCK_DELAY);
  
  // 模拟随机性：50%概率返回今日数据，50%概率返回昨日数据
  const useYesterday = Math.random() > 0.5;
  
  if (useYesterday) {
    // 返回昨天的模拟数据
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    
    return {
      ...mockTodayGame,
      opponent: '凯尔特人',
      date: yesterday.toISOString().split('T')[0],
      result: 'L',
      points: 24,
      rebounds: 11,
      assists: 8,
      steals: 1,
      blocks: 0,
      minutes: 38,
      fgPercent: 48.5,
      threePercent: 33.3,
      ftPercent: 90.0,
    };
  }
  
  return mockTodayGame;
}

/**
 * Mock API: 获取生涯统计数据
 * GET /api/career-stats
 */
export async function mockFetchCareerStats(): Promise<{
  stats: CareerStats;
  rankings: RankingData[];
}> {
  await delay(MOCK_DELAY);
  
  // 模拟动态数据：基于当前日期微调得分
  const today = new Date();
  const daysSinceEpoch = Math.floor(today.getTime() / (1000 * 60 * 60 * 24));
  const dynamicPoints = mockCareerStats.points + (daysSinceEpoch % 10); // 每天增加0-9分
  
  // 更新得分排名差距
  const updatedRankings = mockRankings.map(ranking => {
    if (ranking.category === '总得分') {
      return {
        ...ranking,
        careerValue: dynamicPoints,
        gapToPrev: ranking.gapToPrev + (daysSinceEpoch % 10),
      };
    }
    return ranking;
  });
  
  return {
    stats: {
      ...mockCareerStats,
      points: dynamicPoints,
    },
    rankings: updatedRankings,
  };
}

/**
 * Mock API: 获取所有数据
 * GET /api/all-stats
 */
export async function mockFetchAllStats(): Promise<{
  todayGame: TodayGameStats;
  career: { stats: CareerStats; rankings: RankingData[] };
}> {
  await delay(MOCK_DELAY);
  
  const [todayGame, career] = await Promise.all([
    mockFetchTodayGame(),
    mockFetchCareerStats(),
  ]);
  
  return {
    todayGame,
    career,
  };
}

/**
 * Mock API: 模拟错误情况
 * 用于测试错误处理
 */
export async function mockFetchWithError(): Promise<never> {
  await delay(MOCK_DELAY);
  throw new Error('模拟网络错误：无法连接到服务器');
}

/**
 * Mock API: 模拟空数据
 * 用于测试无比赛日情况
 */
export async function mockFetchEmptyGame(): Promise<TodayGameStats | null> {
  await delay(MOCK_DELAY);
  return null;
}

// 导出所有Mock API函数
export const mockApi = {
  fetchTodayGame: mockFetchTodayGame,
  fetchCareerStats: mockFetchCareerStats,
  fetchAllStats: mockFetchAllStats,
  fetchWithError: mockFetchWithError,
  fetchEmptyGame: mockFetchEmptyGame,
};

export default mockApi;
