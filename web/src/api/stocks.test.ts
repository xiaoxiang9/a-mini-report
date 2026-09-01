import { describe, expect, it } from 'vitest';
import { addTrackedStock, fetchTrackedStocks, searchStocks } from './stocks';

describe('stock tracking api', () => {
  it('requests the tracking list', async () => {
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (input) => new Response(JSON.stringify([]), { status: 200, headers: { 'content-type': 'application/json' } });
    await expect(fetchTrackedStocks()).resolves.toEqual([]);
    globalThis.fetch = originalFetch;
  });

  it('posts a stock code when adding a stock', async () => {
    let capturedBody = '';
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (_input, init) => { capturedBody = String(init?.body); return new Response('{}', { status: 201 }); };
    await addTrackedStock('600519.SH');
    globalThis.fetch = originalFetch;
    expect(capturedBody).toBe(JSON.stringify({ tsCode: '600519.SH' }));
  });

  it('searches stocks through the same-origin API path', async () => {
    let capturedUrl = '';
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async (input) => { capturedUrl = String(input); return new Response('[]', { status: 200 }); };
    await expect(searchStocks('贵州')).resolves.toEqual([]);
    globalThis.fetch = originalFetch;
    expect(capturedUrl).toContain('/api/stocks/search?q=%E8%B4%B5%E5%B7%9E');
  });
});
