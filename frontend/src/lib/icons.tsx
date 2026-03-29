/**
 * lucide-react 图标扩展模块
 * 
 * 提供自定义 Basketball 图标，并重新导出所有 lucide-react 图标
 */

// 自定义 Basketball 图标组件
export const Basketball = ({ 
  className = "", 
  size = 24, 
  color = "currentColor",
  strokeWidth = 2 
}: {
  className?: string;
  size?: number | string;
  color?: string;
  strokeWidth?: number | string;
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth={strokeWidth}
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="2" x2="12" y2="22" />
    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
    <line x1="2" y1="12" x2="22" y2="12" />
    <line x1="19.07" y1="4.93" x2="4.93" y2="19.07" />
    <path d="M12 2a10 10 0 0 1 10 10" />
  </svg>
);

// 重新导出所有 lucide-react 图标
export * from 'lucide-react';
