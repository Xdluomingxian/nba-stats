import { useStats } from './hooks/useStats';
import { formatNumber, formatGap, translateResult, getResultColor } from './types/stats';
import { Trophy, TrendingUp, Award, Calendar, Clock, Target } from 'lucide-react';

/**
 * 今日战报卡片组件
 */
function TodayGameCard() {
  const { todayGame, loading } = useStats();

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-2xl p-6 animate-pulse">
        <div className="h-6 bg-purple-700 rounded w-1/3 mb-4"></div>
        <div className="h-4 bg-purple-700 rounded w-1/4 mb-2"></div>
        <div className="h-4 bg-purple-700 rounded w-1/4"></div>
      </div>
    );
  }

  if (!todayGame) {
    return (
      <div className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-2xl p-6 text-center">
        <Calendar className="w-12 h-12 mx-auto mb-4 text-yellow-400" />
        <h3 className="text-xl font-bold mb-2">暂无比赛</h3>
        <p className="text-gray-300">今日没有比赛安排</p>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-2xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-bold flex items-center">
          <Calendar className="w-6 h-6 mr-2 text-yellow-400" />
          最新战报
        </h3>
        <span className={`px-4 py-2 rounded-full font-bold ${getResultColor(todayGame.result)} bg-white/10`}>
          {translateResult(todayGame.result)}
        </span>
      </div>

      <div className="mb-4">
        <div className="text-3xl font-bold mb-2">vs {todayGame.opponent}</div>
        <div className="text-gray-300">{todayGame.date}</div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="text-center">
          <div className="text-3xl font-bold text-yellow-400">{todayGame.points}</div>
          <div className="text-sm text-gray-300">得分</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-400">{todayGame.rebounds}</div>
          <div className="text-sm text-gray-300">篮板</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-400">{todayGame.assists}</div>
          <div className="text-sm text-gray-300">助攻</div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-white/10 grid grid-cols-3 gap-2 text-sm">
        <div className="text-center">
          <div className="text-gray-300">投篮</div>
          <div className="font-bold">{todayGame.fgPercent}%</div>
        </div>
        <div className="text-center">
          <div className="text-gray-300">三分</div>
          <div className="font-bold">{todayGame.threePercent}%</div>
        </div>
        <div className="text-center">
          <div className="text-gray-300">罚球</div>
          <div className="font-bold">{todayGame.ftPercent}%</div>
        </div>
      </div>
    </div>
  );
}

/**
 * 生涯统计卡片组件
 */
function CareerStatsCard() {
  const { careerStats, loading } = useStats();

  if (loading || !careerStats) {
    return (
      <div className="bg-gradient-to-br from-yellow-900 to-yellow-800 rounded-2xl p-6 animate-pulse">
        <div className="h-6 bg-yellow-700 rounded w-1/3 mb-4"></div>
        <div className="grid grid-cols-2 gap-4">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-16 bg-yellow-700 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  const stats = [
    { label: '出场', value: careerStats.games, icon: '🏀' },
    { label: '得分', value: careerStats.points, icon: '🎯' },
    { label: '篮板', value: careerStats.rebounds, icon: '📊' },
    { label: '助攻', value: careerStats.assists, icon: '✨' },
    { label: '抢断', value: careerStats.steals, icon: '🔥' },
    { label: '盖帽', value: careerStats.blocks, icon: '🛡️' },
    { label: '三双', value: careerStats.tripleDoubles, icon: '👑' },
    { label: '时间', value: formatNumber(careerStats.minutes), icon: '⏱️' },
  ];

  return (
    <div className="bg-gradient-to-br from-yellow-900 to-yellow-800 rounded-2xl p-6 shadow-xl">
      <h3 className="text-2xl font-bold mb-4 flex items-center">
        <Award className="w-6 h-6 mr-2" />
        生涯统计
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="text-center">
            <div className="text-2xl mb-1">{stat.icon}</div>
            <div className="text-2xl font-bold text-yellow-300">{stat.value}</div>
            <div className="text-sm text-gray-300">{stat.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * 历史排名卡片组件
 */
function RankingsCard() {
  const { rankings, loading } = useStats();

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-blue-900 to-blue-800 rounded-2xl p-6 animate-pulse">
        <div className="h-6 bg-blue-700 rounded w-1/3 mb-4"></div>
        {[1, 2, 3, 4, 5].map(i => (
          <div key={i} className="h-12 bg-blue-700 rounded mb-2"></div>
        ))}
      </div>
    );
  }

  const getRankIcon = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <div className="bg-gradient-to-br from-blue-900 to-blue-800 rounded-2xl p-6 shadow-xl">
      <h3 className="text-2xl font-bold mb-4 flex items-center">
        <TrendingUp className="w-6 h-6 mr-2" />
        历史排名
      </h3>
      <div className="space-y-3">
        {rankings.map((ranking) => (
          <div
            key={ranking.category}
            className={`p-4 rounded-xl ${
              ranking.rank === 1 ? 'bg-yellow-500/20 border border-yellow-500/50' : 'bg-white/5'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <span className="text-2xl mr-3">{getRankIcon(ranking.rank)}</span>
                <span className="font-bold text-lg">{ranking.category}</span>
              </div>
              <div className="text-2xl font-bold text-blue-300">
                {formatNumber(ranking.careerValue)}
              </div>
            </div>
            <div className="text-sm text-gray-300 ml-11">
              {formatGap(ranking.rank, ranking.gapToPrev, ranking.prevPlayerName)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * 主页面组件
 */
function App() {
  const { loading, error, refetch, apiHealthy } = useStats();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      {/* 头部 */}
      <header className="bg-black/30 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Trophy className="w-10 h-10 text-yellow-400 mr-3" />
              <div>
                <h1 className="text-3xl font-bold">勒布朗·詹姆斯</h1>
                <p className="text-gray-400">LeBron James · #23 · Los Angeles Lakers</p>
              </div>
            </div>
            <button
              onClick={refetch}
              disabled={loading}
              className="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 disabled:bg-gray-500 rounded-lg font-bold transition-colors"
            >
              {loading ? '加载中...' : '刷新'}
            </button>
          </div>
        </div>
      </header>

      {/* 主要内容 */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* 错误提示 */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-xl">
            <div className="flex items-center">
              <span className="text-2xl mr-2">⚠️</span>
              <div>
                <div className="font-bold">加载失败</div>
                <div className="text-sm">{error}</div>
                {!apiHealthy && (
                  <div className="text-sm mt-2 text-yellow-300">
                    提示：请确保后端 API 服务已启动 (http://localhost:3000)
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* 今日战报 */}
        <section className="mb-8">
          <TodayGameCard />
        </section>

        {/* 生涯统计 */}
        <section className="mb-8">
          <CareerStatsCard />
        </section>

        {/* 历史排名 */}
        <section>
          <RankingsCard />
        </section>
      </main>

      {/* 页脚 */}
      <footer className="bg-black/30 border-t border-white/10 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-400">
          <p>数据来源：NBA Official API</p>
          <p className="text-sm mt-2">最后更新：{new Date().toLocaleString('zh-CN')}</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
