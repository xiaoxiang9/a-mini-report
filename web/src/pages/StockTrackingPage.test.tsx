import { describe, expect, it } from 'vitest';
import { frozenOffset, tableScrollWidth } from './StockTrackingPage';

describe('stock tracking frozen columns', () => {
  it('calculates the left offset from preceding frozen columns', () => {
    const columns = [
      { key: 'stockName', visible: true, frozen: true, searchable: true, searchType: 'text' as const, order: 0 },
      { key: 'tsCode', visible: true, frozen: true, searchable: true, searchType: 'text' as const, order: 1 },
      { key: 'peTtm', visible: true, frozen: false, searchable: true, searchType: 'number' as const, order: 2 },
    ];
    expect(frozenOffset(columns, 0)).toBe(0);
    expect(frozenOffset(columns, 1)).toBe(100);
    expect(frozenOffset(columns, 2)).toBe(280);
    expect(tableScrollWidth(columns)).toBe(510);
  });
});
