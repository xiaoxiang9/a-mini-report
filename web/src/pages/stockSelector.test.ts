import { describe, expect, it } from 'vitest';
import { getAddActionState, selectionToAddCode } from './stockSelector';

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
});
