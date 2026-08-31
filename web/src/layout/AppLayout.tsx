import type { ReactNode } from 'react';
import { NavLink, useLocation } from 'react-router-dom';

const navigation = [
  { to: '/', label: '总览', glyph: '◈', end: true },
  { to: '/daily-review', label: '每日复盘', glyph: '↗' },
  { to: '/stock-tracking', label: '个股追踪', glyph: '◎' },
  { to: '/strategy-selection', label: '策略选股', glyph: '⌁' },
  { to: '/tasks', label: '任务管理', glyph: '◷' },
];

export function AppLayout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation();
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">A</span><span><b>A-STOCK</b><small>STRATEGY DESK</small></span></div>
      <div className="sidebar-section-label">WORKSPACE</div>
      <nav className="main-nav">{navigation.map((item) => <NavLink key={item.to} to={item.to} end={item.end} className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}><span className="nav-glyph">{item.glyph}</span>{item.label}{item.label !== '总览' && <span className="nav-dot">{item.label === '每日复盘' ? 'LIVE' : item.label === '任务管理' ? 'ADMIN' : 'SOON'}</span>}</NavLink>)}</nav>
      <div className="sidebar-footer"><span className="pulse"></span><span>数据服务在线</span><small>v0.1 / PREVIEW</small></div>
    </aside>
    <main className="main-content"><header className="topbar"><span className="topbar-path">INVESTMENT INTELLIGENCE <i>/</i> {pathname === '/' ? 'OVERVIEW' : pathname.slice(1).toUpperCase()}</span><span className="topbar-date">MARKET DESK <b>·</b> 2026.08.30</span></header>{children}</main>
  </div>;
}
