import { describe, expect, it } from 'vitest';
import { addTrackedStock, fetchTrackedStocks } from './stocks';

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
});
