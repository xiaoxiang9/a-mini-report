export function selectionToAddCode(selection: { tsCode: string } | null): string | null {
  return selection?.tsCode ?? null;
}
