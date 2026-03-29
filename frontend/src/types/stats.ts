// ==================== 基础类型定义 ====================

/**
 * 比赛结果
 */
export type GameResult = 'W' | 'L';

/**
 * 排名类别
 */
export type RankingCategory = 
  | '总得分' 
  | '总助攻' 
  | '总篮板' 
  | '总抢断' 
  | '总盖帽' 
  | '总出场' 
  | '总三双' 
  | '总时间';

// ==================== 数据类型定义 ====================

/**
 * 今日战报数据
 * 对应最近一场比赛的详细统计
 */
export interface TodayGameStats {
  /** 对手球队名称 */
  opponent: string;
  /** 比赛日期，格式：YYYY-MM-DD */
  date: string;
  /** 比赛结果：W=胜利，L=失败 */
  result: GameResult;
  /** 得分 */
  points: number;
  /** 篮板 */
  rebounds: number;
  /** 助攻 */
  assists: number;
  /** 抢断 */
  steals: number;
  /** 盖帽 */
  blocks: number;
  /** 出场时间（分钟） */
  minutes: number;
  /** 投篮命中率（百分比数值，如 52.4 表示 52.4%） */
  fgPercent: number;
  /** 三分命中率 */
  threePercent: number;
  /** 罚球命中率 */
  ftPercent: number;
}

/**
 * 生涯累计数据
 * 常规赛生涯统计数据
 */
export interface CareerStats {
  /** 出场次数 */
  games: number;
  /** 总得分 */
  points: number;
  /** 总篮板 */
  rebounds: number;
  /** 总助攻 */
  assists: number;
  /** 总抢断 */
  steals: number;
  /** 总盖帽 */
  blocks: number;
  /** 总出场时间（分钟） */
  minutes: number;
  /** 三双次数 */
  tripleDoubles: number;
}

/**
 * 历史排名数据
 * 某一项统计数据的历史排名信息
 */
export interface RankingData {
  /** 统计类别 */
  category: RankingCategory;
  /** 生涯累计值 */
  careerValue: number;
  /** 历史排名（1 表示历史第一） */
  rank: number;
  /** 上一名球员（排名更高的那位）名称 */
  prevPlayerName: string;
  /** 上一名球员的数据值 */
  prevPlayerValue: number;
  /** 
   * 与上一名的差距
   * - 正值：领先下一名的数值（如 rank=1 时）
   * - 负值：距离上一名的差距（如 rank>1 时）
   */
  gapToPrev: number;
}

// ==================== API 响应类型 ====================

/**
 * /api/today-game 响应
 */
export type TodayGameResponse = TodayGameStats | null;

/**
 * /api/career-stats 响应
 */
export interface CareerStatsResponse {
  stats: CareerStats;
  rankings: RankingData[];
}

/**
 * /api/all-stats 响应
 */
export interface AllStatsResponse {
  todayGame: TodayGameStats | null;
  career: {
    stats: CareerStats;
    rankings: RankingData[];
  };
}

// ==================== 工具函数 ====================

/**
 * 格式化数字（千分位）
 */
export const formatNumber = (num: number): string => {
  return num.toLocaleString('zh-CN');
};

/**
 * 格式化差距显示
 */
export const formatGap = (rank: number, gapToPrev: number, prevPlayerName: string): string => {
  if (rank === 1) {
    return `领先第 2 名 ${Math.abs(gapToPrev).toLocaleString()}`;
  }
  if (gapToPrev > 0) {
    return `领先第${rank + 1}名 ${Math.abs(gapToPrev).toLocaleString()}`;
  }
  return `距${prevPlayerName}差 ${Math.abs(gapToPrev).toLocaleString()}`;
};

/**
 * 比赛结果翻译
 */
export const translateResult = (result: GameResult): string => {
  return result === 'W' ? '胜' : '负';
};

/**
 * 比赛结果颜色（Tailwind CSS 类名）
 */
export const getResultColor = (result: GameResult): string => {
  return result === 'W' ? 'text-green-400' : 'text-red-400';
};

/**
 * 排名图标
 */
export const getRankIcon = (rank: number): string => {
  if (rank === 1) return '🥇';
  if (rank === 2) return '🥈';
  if (rank === 3) return '🥉';
  return `#${rank}`;
};
