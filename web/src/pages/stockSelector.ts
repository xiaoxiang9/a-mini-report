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
  if (message.includes('FROZEN_COLUMNS_NOT_CONTIGUOUS')) return '冻结列必须从左侧连续设置，请先取消断档列后再保存';
  if (message.includes('IDENTITY_COLUMNS_LOCKED')) return '股票名称和股票代码为固定字段，不允许修改';
  if (message.includes('IDENTITY_COLUMN_REQUIRED')) return '至少保留股票名称或股票代码列';
  if (message.includes('TABLE_COLUMNS_EMPTY')) return '至少保留一个表格字段';
  if (message.includes('404') || message.includes('STOCK_NOT_FOUND')) return '未找到这支股票，请检查名称或代码';
  if (message.includes('422') || message.includes('INVALID_TS_CODE')) return '股票代码格式不正确，请重新搜索并选择结果';
  if (message.includes('503') || message.includes('TUSHARE_')) return '行情数据源暂不可用，请检查 Tushare 配置';
  if (message.includes('Failed to fetch') || message.includes('NetworkError')) return '网络连接失败，请检查网络后重试';
  return '添加失败，请稍后重试';
}
