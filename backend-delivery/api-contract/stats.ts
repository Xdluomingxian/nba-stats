// 今日战报数据
export interface TodayGameStats {
  opponent: string;
  date: string;
  result: string;
  points: number;
  rebounds: number;
  assists: number;
  steals: number;
  blocks: number;
  minutes: number;
  fgPercent: number;
  threePercent: number;
  ftPercent: number;
}

// 生涯累计数据
export interface CareerStats {
  games: number;
  points: number;
  rebounds: number;
  assists: number;
  steals: number;
  blocks: number;
  minutes: number;
  tripleDoubles: number;
}

// 历史排名数据
export interface RankingData {
  category: string;
  careerValue: number;
  rank: number;
  prevPlayerName: string;  // 上一名球员（排名更高的那位）
  prevPlayerValue: number; // 上一名球员的数据
  gapToPrev: number;       // 与上一名的差距
}

// 今日战报数据（示例）
export const todayGameStats: TodayGameStats = {
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

// 生涯累计数据
export const careerStats: CareerStats = {
  games: 1615,
  points: 43241,
  rebounds: 11992,
  assists: 11904,
  steals: 2319,
  blocks: 1147,
  minutes: 59390,
  tripleDoubles: 122,
};

// 历史排名数据
export const rankings: RankingData[] = [
  {
    category: '总得分',
    careerValue: 43241,
    rank: 1,
    prevPlayerName: '贾巴尔',
    prevPlayerValue: 38387,
    gapToPrev: 4854,  // 领先第2名4854分
  },
  {
    category: '总助攻',
    careerValue: 11904,
    rank: 4,
    prevPlayerName: '纳什',
    prevPlayerValue: 10335,
    gapToPrev: -1569, // 距第3名纳什还差1569次
  },
  {
    category: '总篮板',
    careerValue: 11992,
    rank: 23,
    prevPlayerName: '瑟蒙德',
    prevPlayerValue: 14464,
    gapToPrev: -2472, // 距第22名还差2472个
  },
  {
    category: '总抢断',
    careerValue: 2319,
    rank: 8,
    prevPlayerName: '奇克斯',
    prevPlayerValue: 2310,
    gapToPrev: 9,     // 领先第9名9次
  },
  {
    category: '总盖帽',
    careerValue: 1147,
    rank: 78,
    prevPlayerName: '吉尔摩尔',
    prevPlayerValue: 1178,
    gapToPrev: -31,   // 距第77名还差31个
  },
  {
    category: '总出场',
    careerValue: 1615,
    rank: 1,
    prevPlayerName: '帕里什',
    prevPlayerValue: 1611,
    gapToPrev: 4,     // 领先第2名4场
  },
  {
    category: '总三双',
    careerValue: 122,
    rank: 5,
    prevPlayerName: '伯德',
    prevPlayerValue: 59,
    gapToPrev: 63,    // 领先第6名63次
  },
  {
    category: '总时间',
    careerValue: 59390,
    rank: 2,
    prevPlayerName: '贾巴尔',
    prevPlayerValue: 66298,
    gapToPrev: -6908, // 距第1名还差6908分钟
  },
];

// 格式化数字
export const formatNumber = (num: number): string => {
  return num.toLocaleString('zh-CN');
};

// 格式化差距显示
export const formatGap = (rank: number, gapToPrev: number, prevPlayerName: string): string => {
  if (rank === 1) {
    return `领先第2名 ${Math.abs(gapToPrev).toLocaleString()}`;
  }
  if (gapToPrev > 0) {
    return `领先第${rank + 1}名 ${Math.abs(gapToPrev).toLocaleString()}`;
  }
  return `距${prevPlayerName}差 ${Math.abs(gapToPrev).toLocaleString()}`;
};
