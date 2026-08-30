import { describe, expect, it } from 'vitest';
import { normalizeHomeSummary } from './home';

describe('normalizeHomeSummary', () => {
  it('keeps the stable home summary contract', () => {
    expect(normalizeHomeSummary({ productName: 'A股投资策略平台', tagline: '用数据，看清每一次市场波动', statusText: '今日市场，保持观察', features: [{ key: 'daily-review', title: '每日复盘', description: '梳理市场脉络', status: 'available' }] })).toEqual({ productName: 'A股投资策略平台', tagline: '用数据，看清每一次市场波动', statusText: '今日市场，保持观察', features: [{ key: 'daily-review', title: '每日复盘', description: '梳理市场脉络', status: 'available' }] });
  });

  it('rejects an incomplete API response', () => {
    expect(() => normalizeHomeSummary({ productName: 'A股投资策略平台' })).toThrow('INVALID_HOME_SUMMARY');
  });
});
