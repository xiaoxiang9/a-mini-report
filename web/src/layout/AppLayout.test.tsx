import { renderToStaticMarkup } from 'react-dom/server';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { App } from '../App';

describe('AppLayout', () => {
  it('renders platform navigation and coming-soon modules', () => {
    const html = renderToStaticMarkup(<MemoryRouter><App /></MemoryRouter>);
    expect(html).toContain('A股投资策略平台');
    expect(html).toContain('每日复盘');
    expect(html).toContain('个股追踪');
    expect(html).toContain('策略选股');
    expect(html).toContain('即将上线');
  });
});
