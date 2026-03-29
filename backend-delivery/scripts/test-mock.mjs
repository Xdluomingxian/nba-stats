// Mock API 测试脚本
// 用于验证Mock服务是否正常工作

import { mockApi } from '../src/mock/mockApi';

console.log('🧪 开始测试 Mock API 服务...\n');

async function testMockApi() {
  try {
    // 测试 1: 获取今日战报
    console.log('📊 测试 1: 获取今日战报 (mockFetchTodayGame)');
    const todayGame = await mockApi.fetchTodayGame();
    console.log('✅ 成功:', JSON.stringify(todayGame, null, 2));
    console.log();

    // 测试 2: 获取生涯统计数据
    console.log('📈 测试 2: 获取生涯统计数据 (mockFetchCareerStats)');
    const careerStats = await mockApi.fetchCareerStats();
    console.log('✅ 成功:', JSON.stringify(careerStats, null, 2));
    console.log();

    // 测试 3: 获取所有数据
    console.log('📦 测试 3: 获取所有数据 (mockFetchAllStats)');
    const allStats = await mockApi.fetchAllStats();
    console.log('✅ 成功:', JSON.stringify(allStats, null, 2));
    console.log();

    // 测试 4: 模拟空数据
    console.log('📭 测试 4: 模拟空数据 (mockFetchEmptyGame)');
    const emptyGame = await mockApi.fetchEmptyGame();
    console.log('✅ 成功:', emptyGame === null ? '返回 null (正确)' : '返回: ' + JSON.stringify(emptyGame));
    console.log();

    // 验证数据结构
    console.log('🔍 数据验证:');
    console.log(`  - 今日战报包含 ${Object.keys(todayGame).length} 个字段`);
    console.log(`  - 生涯统计包含 ${Object.keys(careerStats.stats).length} 个字段`);
    console.log(`  - 排名数据包含 ${careerStats.rankings.length} 条记录`);
    console.log();

    console.log('✅ 所有 Mock API 测试通过！');
    console.log();
    console.log('📝 当前配置:');
    console.log(`   VITE_USE_MOCK=${process.env.VITE_USE_MOCK || 'true'}`);

  } catch (error) {
    console.error('❌ 测试失败:', error);
    process.exit(1);
  }
}

testMockApi();
