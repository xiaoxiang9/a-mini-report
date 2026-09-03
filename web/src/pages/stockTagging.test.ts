import { describe, expect, it } from 'vitest';
import { filterStocksByTags } from './stockTagging';

const stock = (tags: StockTag[]) => ({ tsCode: '600519.SH', tags } as never);
type StockTag = { id: number; categoryId: number; categoryName: string; name: string };

describe('stock tag filters', () => {
  it('matches the selected second-level tag in each category', () => {
    const stocks = [stock([{ id: 1, categoryId: 10, categoryName: '风格', name: '价值' }]), stock([])];
    expect(filterStocksByTags(stocks, { 10: 1 })).toHaveLength(1);
  });
});
