export function selectionToAddCode(selection: { tsCode: string } | null): string | null {
  return selection?.tsCode ?? null;
}

export function getAddActionState(selection: { tsCode: string } | null, isAdding: boolean) {
  return { disabled: isAdding || !selection, label: isAdding ? '添加中…' : '添加股票' };
}

export function getSearchResultAction(isTracked: boolean, isAdding: boolean) {
  return { disabled: isTracked || isAdding, label: isTracked ? '已添加' : isAdding ? '添加中…' : '添加' };
}

export function formatStockError(error: unknown): string {
  const message = error instanceof Error ? error.message : '';
  if (message.includes('404') || message.includes('STOCK_NOT_FOUND')) return '未找到这支股票，请检查名称或代码';
  if (message.includes('422') || message.includes('INVALID_TS_CODE')) return '股票代码格式不正确，请重新搜索并选择结果';
  if (message.includes('503') || message.includes('TUSHARE_')) return '行情数据源暂不可用，请检查 Tushare 配置';
  if (message.includes('Failed to fetch') || message.includes('NetworkError')) return '网络连接失败，请检查网络后重试';
  return '添加失败，请稍后重试';
}
