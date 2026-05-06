interface StatItemProps {
  label: string;
  value: string | number;
  suffix?: string;
  highlight?: boolean;
  small?: boolean;
}

export const StatItem = ({ label, value, suffix = '', highlight = false, small = false }: StatItemProps) => (
  <div
    className={`flex flex-col items-center rounded-xl border border-white/10 bg-gradient-to-b from-white/10 to-white/5 ${small ? 'p-2' : 'p-4'}`}
  >
    <span className={`mb-1 text-xs uppercase tracking-wider text-white/60 ${small ? 'text-[10px] mb-0.5' : ''}`}>
      {label}
    </span>
    <div className="flex items-baseline gap-1">
      <span
        className={`font-black ${small ? 'text-lg' : 'text-2xl sm:text-3xl'} ${highlight ? 'text-[#FDB927]' : 'text-white'}`}
      >
        {value}
      </span>
      {suffix && <span className="text-sm text-white/50">{suffix}</span>}
    </div>
  </div>
);
