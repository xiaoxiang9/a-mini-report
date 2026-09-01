export interface StockDetail {
  tsCode: string;
  stockName: string;
  exchange: string;
  isTracked: boolean;
  currentPrice: number | null;
  change7dPercent: number | null;
  peTtm: number | null;
  pePercentile: number | null;
  pb: number | null;
  pbPercentile: number | null;
  valuationHistory: Array<{ trade_date: string; pe_ttm: number | null; pb: number | null }>;
  latestTradeDate: string | null;
  dataSource: string | null;
  lastSyncedAt: string | null;
  syncError: string | null;
}
export interface StockSearchResult { tsCode: string; stockName: string; exchange: string; isTracked: boolean; }

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '');

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, init);
  if (!response.ok) {
    let detail = '';
    try { const body = await response.json() as { detail?: string }; detail = body.detail ?? ''; } catch { /* empty response */ }
    throw new Error(`STOCK_API_HTTP_${response.status}_${detail}`);
  }
  return response.json() as Promise<T>;
}

export function fetchTrackedStocks(): Promise<StockDetail[]> {
  return request<StockDetail[]>('/api/stocks/tracking');
}

export function fetchStockDetail(tsCode: string): Promise<StockDetail> {
  return request<StockDetail>(`/api/stocks/${encodeURIComponent(tsCode)}`);
}

export function addTrackedStock(tsCode: string): Promise<StockDetail> {
  return request<StockDetail>('/api/stocks/tracking', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ tsCode }),
  });
}

export function searchStocks(query: string): Promise<StockSearchResult[]> {
  return request<StockSearchResult[]>(`/api/stocks/search?q=${encodeURIComponent(query)}`);
}

export function removeTrackedStock(tsCode: string): Promise<StockDetail> {
  return request<StockDetail>(`/api/stocks/${encodeURIComponent(tsCode)}`, { method: 'DELETE' });
}
