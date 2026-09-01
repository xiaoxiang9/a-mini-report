export function selectionToAddCode(selection: { tsCode: string } | null): string | null {
  return selection?.tsCode ?? null;
}

export function getAddActionState(selection: { tsCode: string } | null, isAdding: boolean) {
  return { disabled: isAdding || !selection, label: isAdding ? '添加中…' : '添加股票' };
}

export function getSearchResultAction(isTracked: boolean, isAdding: boolean) {
  return { disabled: isTracked || isAdding, label: isTracked ? '已添加' : isAdding ? '添加中…' : '添加' };
}
