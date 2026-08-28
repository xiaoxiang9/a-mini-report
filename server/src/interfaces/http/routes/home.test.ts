import { describe, expect, it } from 'vitest';
import { buildApp } from '../app.js';

const summary = {
  productName: 'A股投资策略平台',
  tagline: '用数据，看清每一次市场波动',
  statusText: '今日市场，保持观察',
  features: [{ key: 'daily-review', title: '每日复盘', description: '梳理市场脉络，捕捉关键变化', status: 'available' as const }],
};

describe('HTTP API', () => {
  it('returns the home summary DTO', async () => {
    const app = await buildApp({
      homeSummary: { execute: async () => summary },
      checkDatabase: async () => 'up',
    });
    const response = await app.inject({ method: 'GET', url: '/api/home/summary' });
    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual(summary);
    await app.close();
  });

  it('returns degraded health when MySQL is unavailable', async () => {
    const app = await buildApp({
      homeSummary: { execute: async () => summary },
      checkDatabase: async () => 'down',
    });
    const response = await app.inject({ method: 'GET', url: '/api/health' });
    expect(response.statusCode).toBe(503);
    expect(response.json()).toEqual({ status: 'degraded', database: 'down' });
    await app.close();
  });
});
