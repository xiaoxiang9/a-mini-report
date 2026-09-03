import type { StockDetail } from '../api/stocks';

export function filterStocksByTags(stocks: StockDetail[], selected: Record<number, number | undefined>): StockDetail[] {
  return stocks.filter((stock) => Object.entries(selected).every(([categoryId, tagId]) => {
    if (!tagId) return true;
    return stock.tags.some((tag) => tag.categoryId === Number(categoryId) && tag.id === tagId);
  }));
}
