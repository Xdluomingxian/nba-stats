/**
 * lucide-react 全局类型扩展
 * 
 * 为缺失的 Basketball 图标提供类型定义
 */

import type { LucideIcon } from 'lucide-react';

declare module 'lucide-react' {
  export const Basketball: LucideIcon;
  export const Trophy: LucideIcon;
}

export {};
