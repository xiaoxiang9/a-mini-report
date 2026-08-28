import { describe, expect, it } from 'vitest';
import { GetHomeSummary } from './get-home-summary.js';
import type { HomeSummaryRepository } from '../../domain/platform/home-summary-repository.js';

describe('GetHomeSummary', () => {
  it('returns the home summary provided by the repository', async () => {
    const summary = {
      productName: 'A股投资策略平台',
      tagline: '用数据，看清每一次市场波动',
      statusText: '今日市场，保持观察',
      features: [],
    };
    const repository: HomeSummaryRepository = { find: async () => summary };
    await expect(new GetHomeSummary(repository).execute()).resolves.toEqual(summary);
  });
});
