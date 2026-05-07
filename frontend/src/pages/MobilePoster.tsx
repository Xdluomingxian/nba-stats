import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Trophy, Target, CircleDot } from 'lucide-react';
import { useMemo } from 'react';
import { useStats, type SeasonType } from '@/hooks/useStats';
import { formatDateCN, type RankingData } from '@/data/stats';
import { StatItem, CareerStatWithRank, LoadingState, ErrorState } from '@/components/stats';

// 移动端海报组件
export default function MobilePoster() {
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

  // 将rankings转为Map，避免重复find调用
  const rankingMap = useMemo(() => {
    const map = new Map<string, RankingData>();
    for (const r of rankings) map.set(r.category, r);
    return map;
  }, [rankings]);

  const getRanking = (category: string) => rankingMap.get(category);

  // 根据赛季类型选择数据
  const displayCareerStats = seasonType === 'Playoffs' ? (playoffCareerStats || careerStats) : careerStats;
  const isPlayoffMode = seasonType === 'Playoffs';

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black">
        <LoadingState small />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black">
        <ErrorState message={error} onRetry={refetch} small />
      </div>
    );
  }

  if (!displayCareerStats) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black">
        <ErrorState message="数据加载失败" onRetry={refetch} small />
      </div>
    );
  }

  // 处理无比赛数据的情况
  const hasGameToday = todayGame !== null;

  return (
    <div className="min-h-screen bg-black">
      {/* 顶部图片区域 */}
      <div className="relative h-48 overflow-hidden">
        <img
          src="/images/lebron-purple.jpg"
          alt="LeBron James"
          className="h-full w-full object-cover object-top"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
        <div className="absolute inset-0 bg-gradient-to-br from-[#552583]/60 via-transparent to-[#311557]/60" />

        {/* 标题叠加 */}
        <div className="absolute bottom-3 left-4 right-4">
          {isMock && (
            <span className="mb-1 inline-flex items-center rounded-full border border-blue-500/30 bg-blue-500/20 px-1.5 py-0.5 text-[10px] font-medium text-blue-400">
              MOCK
            </span>
          )}
          <div className="mb-1 flex items-center gap-2">
            <span className="text-xs font-bold tracking-widest text-[#FDB927]">THE KING</span>
            <div className="h-px w-8 bg-[#FDB927]" />
          </div>
          <h1 className="text-2xl font-black leading-none text-white">
            LEBRON
            <span className="text-[#FDB927]"> JAMES</span>
          </h1>
        </div>
      </div>

      {/* 赛季类型切换 */}
      <div className="px-3 -mt-2">
        <Tabs 
          value={seasonType} 
          onValueChange={(value) => setSeasonType(value as SeasonType)}
          className="w-full"
        >
          <TabsList className="grid w-full grid-cols-2 rounded-xl bg-white/5 p-1">
            <TabsTrigger
              value="Regular Season"
              className="py-2 text-sm text-white/70 data-[state=active]:bg-[#FDB927] data-[state=active]:text-black"
            >
              常规赛
            </TabsTrigger>
            <TabsTrigger
              value="Playoffs"
              className="py-2 text-sm text-white/70 data-[state=active]:bg-[#FDB927] data-[state=active]:text-black"
            >
              季后赛
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Tab切换区域 */}
      <div className="-mt-2 px-3">
        <Tabs defaultValue={hasGameToday ? "today" : "career"} className="w-full">
          <TabsList className="grid w-full grid-cols-2 rounded-xl bg-white/5 p-1">
            <TabsTrigger
              value="today"
              className="py-2 text-sm text-white/70 data-[state=active]:bg-[#FDB927] data-[state=active]:text-black"
            >
              {hasGameToday ? "今日战报" : "最近战报"}
            </TabsTrigger>
            <TabsTrigger
              value="career"
              className="py-2 text-sm text-white/70 data-[state=active]:bg-[#FDB927] data-[state=active]:text-black"
            >
              生涯累计 · {isPlayoffMode ? '季后赛' : '常规赛'}
            </TabsTrigger>
          </TabsList>

          {/* 今日/最近战报 */}
          <TabsContent value="today" className="mt-4">
            {hasGameToday ? (
              <Card className="border-white/10 bg-white/5 backdrop-blur-sm">
                <CardHeader className="pb-2">
                  <CardTitle className="flex items-center justify-between text-base text-[#FDB927]">
                    <div className="flex items-center gap-2">
                      <Target className="h-4 w-4" />
                      {isPlayoffMode ? '季后赛战报' : '最近战报'}
                    </div>
                    <span className="text-xs text-white/50">
                      {todayGame.date_local || formatDateCN(todayGame.date)}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* 比赛结果 */}
                  <div className="flex items-center justify-center gap-3 py-2">
                    <div className="text-center">
                      <span className="text-lg font-bold text-white">湖人</span>
                    </div>
                    <span
                      className={`rounded px-2 py-0.5 text-sm font-bold ${
                        todayGame.result === 'W'
                          ? 'bg-green-500/20 text-green-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}
                    >
                      {todayGame.result}
                    </span>
                    <div className="text-center">
                      <span className="text-lg font-bold text-white">{todayGame.opponent}</span>
                    </div>
                  </div>

                  <div className="h-px bg-white/10" />

                  {/* 五项数据 */}
                  <div className="grid grid-cols-5 gap-2">
                    <StatItem label="得分" value={todayGame.points} highlight small />
                    <StatItem label="篮板" value={todayGame.rebounds} small />
                    <StatItem label="助攻" value={todayGame.assists} small />
                    <StatItem label="抢断" value={todayGame.steals} small />
                    <StatItem label="盖帽" value={todayGame.blocks} small />
                  </div>

                  {/* 命中率 */}
                  <div className="grid grid-cols-3 gap-2 pt-2">
                    <div className="rounded-lg bg-white/5 p-2 text-center">
                      <span className="text-xs text-white/50">投篮</span>
                      <span className="ml-1 font-bold text-white">{todayGame.fgPercent}%</span>
                    </div>
                    <div className="rounded-lg bg-white/5 p-2 text-center">
                      <span className="text-xs text-white/50">三分</span>
                      <span className="ml-1 font-bold text-white">{todayGame.threePercent}%</span>
                    </div>
                    <div className="rounded-lg bg-white/5 p-2 text-center">
                      <span className="text-xs text-white/50">罚球</span>
                      <span className="ml-1 font-bold text-white">{todayGame.ftPercent}%</span>
                    </div>
                  </div>

                  <div className="pt-1 text-center text-xs text-white/40">
                    出场时间: {todayGame.minutes}分钟
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="border-white/10 bg-white/5 backdrop-blur-sm">
                <CardContent className="py-12 text-center">
                  <CircleDot className="mx-auto mb-4 h-12 w-12 text-white/30" />
                  <p className="text-sm text-white/50">
                    {isPlayoffMode ? '季后赛暂无比赛' : '休赛期暂无比赛'}
                  </p>
                  <p className="mt-2 text-xs text-white/30">
                    {isPlayoffMode ? '请等待季后赛开始' : '请等待新赛季开始'}
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* 生涯累计 · 整合排名 */}
          <TabsContent value="career" className="mt-4">
            <Card className="border-white/10 bg-white/5 backdrop-blur-sm">
              <CardHeader className="pb-2">
                <CardTitle className="flex items-center gap-2 text-base text-[#FDB927]">
                  <Trophy className="h-4 w-4" />
                  生涯累计 · {isPlayoffMode ? '季后赛' : '常规赛'}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* 第一行：出场、得分、篮板、助攻 */}
                <div className="grid grid-cols-4 gap-2">
                  <CareerStatWithRank small
                    label="出场"
                    value={displayCareerStats.games}
                    rank={getRanking('总出场')?.rank || 1}
                    gapToPrev={getRanking('总出场')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总出场')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank small
                    label="得分"
                    value={displayCareerStats.points}
                    rank={getRanking('总得分')?.rank || 1}
                    gapToPrev={getRanking('总得分')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总得分')?.prevPlayerName || ''}
                    highlight
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank small
                    label="篮板"
                    value={displayCareerStats.rebounds}
                    rank={getRanking('总篮板')?.rank || 23}
                    gapToPrev={getRanking('总篮板')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总篮板')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank small
                    label="助攻"
                    value={displayCareerStats.assists}
                    rank={getRanking('总助攻')?.rank || 4}
                    gapToPrev={getRanking('总助攻')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总助攻')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                </div>

                {/* 第二行：抢断、盖帽、时间、三双 */}
                <div className="grid grid-cols-4 gap-2">
                  <CareerStatWithRank small
                    label="抢断"
                    value={displayCareerStats.steals}
                    rank={getRanking('总抢断')?.rank || 8}
                    gapToPrev={getRanking('总抢断')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总抢断')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank small
                    label="盖帽"
                    value={displayCareerStats.blocks}
                    rank={getRanking('总盖帽')?.rank || 78}
                    gapToPrev={getRanking('总盖帽')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总盖帽')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank small
                    label="时间"
                    value={displayCareerStats.minutes}
                    rank={getRanking('总时间')?.rank || 2}
                    gapToPrev={getRanking('总时间')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总时间')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                  <CareerStatWithRank small
                    label="三双"
                    value={displayCareerStats.tripleDoubles}
                    rank={getRanking('总三双')?.rank || 5}
                    gapToPrev={getRanking('总三双')?.gapToPrev || 0}
                    prevPlayerName={getRanking('总三双')?.prevPlayerName || ''}
                    hideRank={isPlayoffMode}
                  />
                </div>

                {/* 数据说明 */}
                <div className="pt-2 text-center text-[10px] text-white/30">
                  * 以上数据均为NBA{isPlayoffMode ? '季后赛' : '常规赛'}生涯累计
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* 底部装饰 */}
      <div className="flex items-end justify-between px-4 py-6">
        <div className="text-xs text-white/20">
          <p>LOS ANGELES LAKERS</p>
          <p>EST. 2003 · 23 SEASONS</p>
        </div>
        <div className="text-right">
          <p className="text-4xl font-black text-[#FDB927]/30">23</p>
        </div>
      </div>

      {/* 角落装饰 */}
      <div className="pointer-events-none fixed left-4 top-4 h-6 w-6 border-l-2 border-t-2 border-[#FDB927]/50" />
      <div className="pointer-events-none fixed right-4 top-4 h-6 w-6 border-r-2 border-t-2 border-[#FDB927]/50" />
    </div>
  );
}
