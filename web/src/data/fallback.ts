import type { HomeSummary } from '../api/home';

export const fallbackHomeSummary: HomeSummary = {
  productName: 'A股投资策略平台',
  tagline: '用数据，看清每一次市场波动',
  statusText: '今日市场，保持观察',
  features: [
    { key: 'daily-review', title: '每日复盘', description: '梳理市场脉络，捕捉关键变化', status: 'available' },
    { key: 'stock-tracking', title: '个股追踪', description: '持续跟踪关注标的', status: 'coming-soon' },
    { key: 'strategy-selection', title: '策略选股', description: '用规则筛选潜在机会', status: 'coming-soon' },
  ],
};
