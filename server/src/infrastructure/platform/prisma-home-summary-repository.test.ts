import { describe, expect, it } from 'vitest';
import { PrismaHomeSummaryRepository } from './prisma-home-summary-repository.js';

describe('PrismaHomeSummaryRepository', () => {
  it('maps and orders Prisma records into a home summary', async () => {
    const prisma = {
      platformConfig: {
        findFirst: async () => ({
          productName: 'A股投资策略平台',
          tagline: '用数据，看清每一次市场波动',
          statusText: '今日市场，保持观察',
          features: [
            { key: 'strategy-selection', title: '策略选股', description: '用规则筛选潜在机会', status: 'coming-soon', sortOrder: 3 },
            { key: 'daily-review', title: '每日复盘', description: '梳理市场脉络，捕捉关键变化', status: 'available', sortOrder: 1 },
          ],
        }),
      },
    };
    const repository = new PrismaHomeSummaryRepository(prisma as never);
    await expect(repository.find()).resolves.toEqual({
      productName: 'A股投资策略平台',
      tagline: '用数据，看清每一次市场波动',
      statusText: '今日市场，保持观察',
      features: [
        { key: 'daily-review', title: '每日复盘', description: '梳理市场脉络，捕捉关键变化', status: 'available' },
        { key: 'strategy-selection', title: '策略选股', description: '用规则筛选潜在机会', status: 'coming-soon' },
      ],
    });
  });
});
