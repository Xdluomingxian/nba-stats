import { formatNumber, formatGap } from '@/data/stats';

interface CareerStatWithRankProps {
  label: string;
  value: number;
  rank: number;
  gapToPrev: number;
  prevPlayerName: string;
  highlight?: boolean;
  small?: boolean;
}

export const CareerStatWithRank = ({
  label,
  value,
  rank,
  gapToPrev,
  prevPlayerName,
  highlight = false,
  small = false,
}: CareerStatWithRankProps) => (
  <div className="overflow-hidden rounded-xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5">
    <div className={`${small ? 'p-3' : 'p-4'} text-center`}>
      {!small && (
        <span className="mb-1 block text-xs uppercase tracking-wider text-white/60">{label}</span>
      )}
      <span
        className={`${small ? 'text-[10px]' : 'text-xs'} uppercase tracking-wider text-white/60 ${highlight ? 'text-[#FDB927]' : 'text-white'} block ${small ? 'text-xl' : 'text-2xl sm:text-3xl'} font-black`}
      >
        {formatNumber(value)}
      </span>
      {small && (
        <span className="text-[10px] uppercase tracking-wider text-white/60">{label}</span>
      )}
    </div>

    <div className={`border-t border-white/10 bg-black/20 ${small ? 'px-2 py-1.5' : 'px-3 py-2'}`}>
      <div className="flex items-center justify-between">
        <span
          className={`rounded px-2 py-0.5 text-xs font-bold ${
            rank === 1
              ? 'bg-[#FDB927] text-black'
              : rank <= 3
                ? 'bg-white/20 text-[#FDB927]'
                : 'bg-white/10 text-white/70'
          } ${small ? 'px-1.5 py-0.5 text-[10px]' : ''}`}
        >
          #{rank}
        </span>
        <span className={`text-xs ${rank === 1 ? 'text-[#FDB927]' : 'text-white/60'} ${small ? 'text-[10px]' : ''}`}>
          {formatGap(rank, gapToPrev, prevPlayerName)}
        </span>
      </div>
    </div>
  </div>
);
