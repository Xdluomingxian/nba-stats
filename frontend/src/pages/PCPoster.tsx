import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Trophy, Target, CircleDot } from 'lucide-react';
import { useMemo } from 'react';
import { useStats, type SeasonType } from '@/hooks/useStats';
import { formatDateCN, type RankingData } from '@/data/stats';
import { StatItem, CareerStatWithRank, LoadingState, ErrorState } from '@/components/stats';

// PC端海报组件
export default function PCPoster() {
  const { 
    todayGame, 
    careerStats, 
    playoffCareerStats,
    rankings, 
    loading, 
    error, 
    refetch, 
    isMock,
    seasonType,
    setSeasonType
  } = useStats();

  // 将rankings转为Map，必须在提前返回之前调用（React hooks规则）
  const rankingMap = useMemo(() => {
    const map = new Map<string, RankingData>();
    for (const r of rankings) map.set(r.category, r);
    return map;
  }, [rankings]);

  // 根据赛季类型选择数据
  const displayCareerStats = seasonType === 'Playoffs' ? (playoffCareerStats || careerStats) : careerStats;
  const isPlayoffMode = seasonType === 'Playoffs';

  if (loading) return <LoadingState />;
  if (error) return <ErrorState message={error} onRetry={refetch} />;
  if (!displayCareerStats) return <ErrorState message="数据加载失败" onRetry={refetch} />;

  const getRanking = (category: string) => rankingMap.get(category);
  
  // 处理无比赛数据的情况
  const hasGameToday = todayGame !== null;

  return (
    <div className="flex min-h-screen items-center justify-center bg-black p-4 lg:p-8">
      <div
        className="relative w-full max-w-7xl overflow-hidden rounded-3xl shadow-2xl"
        style={{ aspectRatio: '16/10', minHeight: '700px' }}
      >
        {/* 背景渐变 */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#552583] via-[#311557] to-[#1a0b2e]" />

        {/* 金色光效 */}
        <div className="bg-gradient-radial absolute right-0 top-0 h-2/3 w-2/3 from-[#FDB927]/30 via-transparent to-transparent blur-3xl" />
        <div className="bg-gradient-radial absolute bottom-0 left-0 h-1/2 w-1/2 from-[#552583]/50 via-transparent to-transparent blur-3xl" />

        {/* 动态线条背景 */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute left-0 top-1/4 h-px w-full bg-gradient-to-r from-transparent via-[#FDB927] to-transparent" />
          <div className="absolute left-0 top-1/2 h-px w-full bg-gradient-to-r from-transparent via-[#FDB927] to-transparent" />
          <div className="absolute left-0 top-3/4 h-px w-full bg-gradient-to-r from-transparent via-[#FDB927] to-transparent" />
        </div>

        {/* 左侧詹姆斯图片区域 */}
        <div className="absolute bottom-0 left-0 h-full w-2/5">
          <img
            src="/images/lebron-purple.jpg"
            alt="LeBron James"
            className="h-full w-full object-cover object-top opacity-90"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-transparent to-[#311557]" />
          <div className="absolute inset-0 bg-gradient-to-t from-[#311557] via-transparent to-transparent" />
        </div>

        {/* 右侧内容区域 */}
        <div className="absolute right-0 top-0 h-full w-3/5 overflow-y-auto p-6 lg:p-10">
          <div className="flex h-full flex-col gap-5">
            {/* 顶部标题 */}
            <div className="mb-2 text-right">
              {isMock && (
                <span className="mb-2 inline-flex items-center rounded-full border border-blue-500/30 bg-blue-500/20 px-2 py-0.5 text-xs font-medium text-blue-400">
                  MOCK数据
                </span>
              )}
              <div className="mb-2 flex items-center justify-end gap-3">
                <span className="text-sm font-bold tracking-widest text-[#FDB927]">THE KING</span>
                <div className="h-px w-12 bg-[#FDB927]" />
              </div>
              <h1 className="text-5xl font-black leading-none tracking-tight text-white lg:text-6xl">
                LEBRON
                <span className="block text-[#FDB927]">JAMES</span>
              </h1>
              <p className="mt-2 text-sm font-light text-white/70">看一场，少一场。致敬传奇。</p>
              
              {/* 赛季类型切换 */}
              <div className="mt-3 flex justify-end">
                <Tabs 
                  value={seasonType} 
                  onValueChange={(value) => setSeasonType(value as SeasonType)}
                  className="w-auto"
                >
                  <TabsList className="grid w-full grid-cols-2 rounded-xl bg-white/5 p-1">
                    <TabsTrigger
                      value="Regular Season"
                      className="px-4 py-2 text-sm text-white/70 data-[state=active]:bg-[#FDB927] data-[state=active]:text-black"
                    >
                      常规赛
                    </TabsTrigger>
                    <TabsTrigger
                      value="Playoffs"
                      className="px-4 py-2 text-sm text-white/70 data-[state=active]:bg-[#FDB927] data-[state=active]:text-black"
                    >
                      季后赛
                    </TabsTrigger>
                  </TabsList>
                </Tabs>
              </div>
            </div>

            {/* 战报 */}
            <Card className="border-white/10 bg-white/5 backdrop-blur-sm">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-lg text-[#FDB927]">
                  <Target className="h-5 w-5" />
                  {isPlayoffMode ? '季后赛战报' : '最近战报'}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {hasGameToday && todayGame ? (
                  <>
                    <div className="mb-4 flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-white">湖人</span>
                        <span
                          className={`rounded px-2 py-0.5 text-sm font-bold ${
                            todayGame.result === 'W'
                              ? 'bg-green-500/20 text-green-400'
                              : 'bg-red-500/20 text-red-400'
                          }`}
                        >
                          {todayGame.result}
                        </span>
                        <span className="text-white/60">vs</span>
                        <span className="font-semibold text-white">{todayGame.opponent}</span>
                      </div>
                      <span className="text-sm text-white/50">{todayGame.minutes}分钟</span>
                    </div>

                    <div className="grid grid-cols-5 gap-3">
                      <StatItem label="得分" value={todayGame.points} highlight />
                      <StatItem label="篮板" value={todayGame.rebounds} />
                      <StatItem label="助攻" value={todayGame.assists} />
                      <StatItem label="抢断" value={todayGame.steals} />
                      <StatItem label="盖帽" value={todayGame.blocks} />
                    </div>

                    <div className="mt-4 flex justify-center gap-6 border-t border-white/10 pt-3">
                      <div className="text-center">
                        <span className="text-xs text-white/50">投篮</span>
                        <span className="ml-2 font-semibold text-white">{todayGame.fgPercent}%</span>
                      </div>
                      <div className="text-center">
                        <span className="text-xs text-white/50">三分</span>
                        <span className="ml-2 font-semibold text-white">{todayGame.threePercent}%</span>
                      </div>
                      <div className="text-center">
                        <span className="text-xs text-white/50">罚球</span>
                        <span className="ml-2 font-semibold text-white">{todayGame.ftPercent}%</span>
                      </div>
                    </div>
                    
                    <div className="mt-2 text-center text-xs text-white/40">
                      比赛日期: {todayGame.date_local || formatDateCN(todayGame.date)}
                    </div>
                  </>
                ) : (
                  <div className="py-8 text-center">
                    <CircleDot className="mx-auto mb-4 h-12 w-12 text-white/30" />
                    <p className="text-sm text-white/50">
                      {isPlayoffMode ? '季后赛暂无比赛' : '休赛期暂无比赛'}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* 生涯累计 */}
            <Card className="flex-1 border-white/10 bg-white/5 backdrop-blur-sm">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-lg text-[#FDB927]">
                  <Trophy className="h-5 w-5" />
                  生涯累计 · {isPlayoffMode ? '季后赛' : '常规赛'}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {/* 第一行：出场、得分、篮板、助攻 */}
                <div className="mb-3 grid grid-cols-4 gap-3">
                  <CareerStatWithRank
                    label="出场"
                    value={displayCareerStats.games}
                    rank={getRanking('总出场')?.rank || 1}
                    gapToPrev={getRanking('总出场')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总出场')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank
                    label="得分"
                    value={displayCareerStats.points}
                    rank={getRanking('总得分')?.rank || 1}
                    gapToPrev={getRanking('总得分')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总得分')?.prevPlayerName || ''}
                    highlight
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank
                    label="篮板"
                    value={displayCareerStats.rebounds}
                    rank={getRanking('总篮板')?.rank || 23}
                    gapToPrev={getRanking('总篮板')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总篮板')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank
                    label="助攻"
                    value={displayCareerStats.assists}
                    rank={getRanking('总助攻')?.rank || 4}
                    gapToPrev={getRanking('总助攻')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总助攻')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                </div>

                {/* 第二行：抢断、盖帽、时间、三双 */}
                <div className="grid grid-cols-4 gap-3">
                  <CareerStatWithRank
                    label="抢断"
                    value={displayCareerStats.steals}
                    rank={getRanking('总抢断')?.rank || 8}
                    gapToPrev={getRanking('总抢断')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总抢断')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank
                    label="盖帽"
                    value={displayCareerStats.blocks}
                    rank={getRanking('总盖帽')?.rank || 78}
                    gapToPrev={getRanking('总盖帽')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总盖帽')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank
                    label="时间"
                    value={displayCareerStats.minutes}
                    rank={getRanking('总时间')?.rank || 2}
                    gapToPrev={getRanking('总时间')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总时间')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank
                    label="三双"
                    value={displayCareerStats.tripleDoubles}
                    rank={getRanking('总三双')?.rank || 5}
                    gapToPrev={getRanking('总三双')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总三双')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* 角落装饰 */}
        <div className="absolute left-4 top-4 h-10 w-10 border-l-2 border-t-2 border-[#FDB927]/50" />
        <div className="absolute right-4 top-4 h-10 w-10 border-r-2 border-t-2 border-[#FDB927]/50" />
        <div className="absolute bottom-4 left-4 h-10 w-10 border-b-2 border-l-2 border-[#FDB927]/50" />
        <div className="absolute bottom-4 right-4 h-10 w-10 border-b-2 border-r-2 border-[#FDB927]/50" />

        {/* 底部装饰 */}
        <div className="pointer-events-none absolute bottom-4 left-4 right-4 flex items-end justify-between">
          <div className="text-xs text-white/20">
            <p>LOS ANGELES LAKERS</p>
            <p>EST. 2003 · 23 SEASONS</p>
          </div>
          <div className="text-right">
            <p className="text-6xl font-black text-[#FDB927]/30">23</p>
          </div>
        </div>
      </div>
    </div>
  );
}
