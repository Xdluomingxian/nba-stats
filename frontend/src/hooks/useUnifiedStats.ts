// useUnifiedStats 已合并至 useStats
// useStats hook 内部已根据 VITE_USE_MOCK 环境变量自动切换 Mock/Real 数据
// 直接使用 import { useStats } from '@/hooks/useStats' 即可

export { useStats } from './useStats';
export default useStats;
