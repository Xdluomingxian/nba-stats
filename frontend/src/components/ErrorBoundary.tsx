import { Component, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-black p-4">
          <div className="max-w-lg rounded-xl border border-red-500/30 bg-red-900/20 p-6 text-center">
            <h2 className="mb-2 text-xl font-bold text-red-400">页面出错了</h2>
            <p className="mb-4 text-sm text-white/60">{this.state.error?.message || '未知错误'}</p>
            <pre className="max-h-40 overflow-auto rounded bg-black/30 p-3 text-left text-xs text-white/40">
              {this.state.error?.stack}
            </pre>
            <button
              className="mt-4 rounded-lg bg-[#FDB927] px-4 py-2 text-sm font-semibold text-black hover:bg-[#FDB927]/80"
              onClick={() => window.location.reload()}
            >
              刷新页面
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
