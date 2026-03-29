// Mock API 测试数据
// 用于本地开发和前端预览

import type { TodayGameStats, CareerStats, RankingData } from '../data/stats';

// 模拟今日战报数据
export const mockTodayGame: TodayGameStats = {
  opponent: '勇士',
  date: '2025-03-28',
  result: 'W',
  points: 28,
  rebounds: 8,
  assists: 6,
  steals: 2,
  blocks: 1,
  minutes: 34,
  fgPercent: 52.4,
  threePercent: 40.0,
  ftPercent: 85.7,
};

// 多组模拟数据（用于测试不同场景）
export const mockTodayGames: TodayGameStats[] = [
  {
    opponent: '勇士',
    date: '2025-03-28',
    result: 'W',
    points: 28,
    rebounds: 8,
    assists: 6,
    steals: 2,
    blocks: 1,
    minutes: 34,
    fgPercent: 52.4,
    threePercent: 40.0,
    ftPercent: 85.7,
  },
  {
    opponent: '凯尔特人',
    date: '2025-03-26',
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
  },
  {
    opponent: '雄鹿',
    date: '2025-03-24',
    result: 'W',
    points: 35,
    rebounds: 7,
    assists: 12,
    steals: 3,
    blocks: 1,
    minutes: 36,
    fgPercent: 58.3,
    threePercent: 45.5,
    ftPercent: 88.9,
  },
];

// 模拟生涯统计数据
export const mockCareerStats: CareerStats = {
  games: 1615,
  points: 43241,
  rebounds: 11992,
  assists: 11904,
  steals: 2319,
  blocks: 1147,
  minutes: 59390,
  tripleDoubles: 122,
};

// 模拟历史排名数据
export const mockRankings: RankingData[] = [
  {
    category: '总得分',
    careerValue: 43241,
    rank: 1,
    prevPlayerName: '贾巴尔',
    prevPlayerValue: 38387,
    gapToPrev: 4854,
  },
  {
    category: '总助攻',
    careerValue: 11904,
    rank: 4,
    prevPlayerName: '纳什',
    prevPlayerValue: 10335,
    gapToPrev: -1569,
  },
  {
    category: '总篮板',
    careerValue: 11992,
    rank: 23,
    prevPlayerName: '瑟蒙德',
    prevPlayerValue: 14464,
    gapToPrev: -2472,
  },
  {
    category: '总抢断',
    careerValue: 2319,
    rank: 8,
    prevPlayerName: '奇克斯',
    prevPlayerValue: 2310,
    gapToPrev: 9,
  },
  {
    category: '总盖帽',
    careerValue: 1147,
    rank: 78,
    prevPlayerName: '吉尔摩尔',
    prevPlayerValue: 1178,
    gapToPrev: -31,
  },
  {
    category: '总出场',
    careerValue: 1615,
    rank: 1,
    prevPlayerName: '帕里什',
    prevPlayerValue: 1611,
    gapToPrev: 4,
  },
  {
    category: '总三双',
    careerValue: 122,
    rank: 5,
    prevPlayerName: '伯德',
    prevPlayerValue: 59,
    gapToPrev: 63,
  },
  {
    category: '总时间',
    careerValue: 59390,
    rank: 2,
    prevPlayerName: '贾巴尔',
    prevPlayerValue: 66298,
    gapToPrev: -6908,
  },
];

// 完整的Mock响应数据
export const mockApiResponses = {
  // GET /api/today-game
  todayGame: mockTodayGame,
  
  // GET /api/career-stats
  careerStats: {
    stats: mockCareerStats,
    rankings: mockRankings,
  },
  
  // GET /api/all-stats
  allStats: {
    todayGame: mockTodayGame,
    career: {
      stats: mockCareerStats,
      rankings: mockRankings,
    },
  },
};

// 导出默认的Mock数据
export default mockApiResponses;
