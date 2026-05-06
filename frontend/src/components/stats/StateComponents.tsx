interface LoadingStateProps {
  small?: boolean;
}

export const LoadingState = ({ small = false }: LoadingStateProps) => (
  <div className="flex h-32 items-center justify-center">
    <div className={`animate-spin rounded-full border-b-2 border-[#FDB927] ${small ? 'h-6 w-6' : 'h-8 w-8'}`}></div>
    <span className={`text-white/60 ${small ? 'ml-2 text-sm' : 'ml-3'}`}>加载中...</span>
  </div>
);

interface ErrorStateProps {
  message: string;
  onRetry: () => void;
  small?: boolean;
}

export const ErrorState = ({ message, onRetry, small = false }: ErrorStateProps) => (
  <div className={`flex h-32 flex-col items-center justify-center ${small ? 'px-4' : ''} text-center`}>
    <p className={`mb-2 text-red-400 ${small ? 'text-sm' : ''}`}>{message}</p>
    <button
      onClick={onRetry}
      className={`rounded-lg bg-[#FDB927] font-semibold text-black transition-colors hover:bg-[#FDB927]/80 ${small ? 'px-3 py-1.5 text-xs' : 'px-4 py-2 text-sm'}`}
    >
      重试
    </button>
  </div>
);
