import type { TodayGameStats, CareerStats, RankingData, AllStatsResponse } from '../types/stats';

// API 基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const REQUEST_TIMEOUT = 10000; // 10 秒超时
const MAX_RETRIES = 3; // 最大重试次数

/**
 * 带超时的 fetch
 */
async function fetchWithTimeout(url: string, options: RequestInit = {}): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * 带重试的 fetch
 */
async function fetchWithRetry(
  url: string, 
  options: RequestInit = {}, 
  maxRetries = MAX_RETRIES
): Promise<Response> {
  let lastError: Error | null = null;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetchWithTimeout(url, options);
      
      // 5xx 错误可重试
      if (response.status >= 500 && i < maxRetries - 1) {
        lastError = new Error(`Server error: ${response.status}`);
        // 指数退避
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        continue;
      }
      
      return response;
    } catch (error) {
      lastError = error as Error;
      
      // 超时或网络错误时重试
      if (error instanceof Error && error.name === 'AbortError') {
        console.warn(`请求超时，第 ${i + 1} 次重试`);
      }
      
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
      }
    }
  }
  
  throw lastError || new Error('Request failed');
}

/**
 * 获取今日战报
 */
export async function fetchTodayGame(): Promise<TodayGameStats | null> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/today-game`);
    
    if (!response.ok) {
      if (response.status === 204) return null;
      throw new Error(`Failed to fetch today game: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching today game:', error);
    throw error; // 抛出异常，由 useStats 统一处理
  }
}

/**
 * 获取生涯统计数据
 */
export async function fetchCareerStats(): Promise<{ stats: CareerStats; rankings: RankingData[] }> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/career-stats`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch career stats: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching career stats:', error);
    throw error;
  }
}

/**
 * 获取所有数据（批量接口）
 */
export async function fetchAllStats(): Promise<AllStatsResponse> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/all-stats`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch all stats: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching all stats:', error);
    throw error;
  }
}

/**
 * 健康检查
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/health`, { 
      cache: 'no-cache' 
    });
    return response.ok;
  } catch {
    return false;
  }
}
