import { describe, expect, it } from 'vitest';
import { formatStockError, getAddActionState, getSearchResultAction, selectionToAddCode } from './stockSelector';

describe('stock selector', () => {
  it('does not produce an add code before a suggestion is selected', () => {
    expect(selectionToAddCode(null)).toBeNull();
  });

  it('produces the selected stock code for submission', () => {
    expect(selectionToAddCode({ tsCode: '600519.SH' })).toBe('600519.SH');
  });

  it('disables the add action and shows progress while adding', () => {
    expect(getAddActionState({ tsCode: '600519.SH' }, true)).toEqual({ disabled: true, label: '添加中…' });
  });

  it('shows added state for tracked search results', () => {
    expect(getSearchResultAction(true, false)).toEqual({ disabled: true, label: '已添加' });
  });

  it('explains common add failures inside the modal', () => {
    expect(formatStockError(new Error('STOCK_API_HTTP_404_STOCK_NOT_FOUND'))).toBe('未找到这支股票，请检查名称或代码');
    expect(formatStockError(new Error('STOCK_API_HTTP_503_TUSHARE_TOKEN_MISSING'))).toBe('行情数据源暂不可用，请检查 Tushare 配置');
  });
});
