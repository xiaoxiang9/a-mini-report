import type { ReactNode } from 'react';
import { CalendarOutlined, DashboardOutlined, FundOutlined, LineChartOutlined, SettingOutlined } from '@ant-design/icons';
import { Layout, Menu, Space, Tag, Typography } from 'antd';
import { NavLink, useLocation } from 'react-router-dom';

const { Header, Sider, Content } = Layout;
const navigation = [
  { to: '/', label: '总览', icon: <DashboardOutlined />, end: true },
  { to: '/daily-review', label: '每日复盘', icon: <CalendarOutlined /> },
  { to: '/stock-tracking', label: '个股追踪', icon: <LineChartOutlined /> },
  { to: '/strategy-selection', label: '策略选股', icon: <FundOutlined /> },
  { to: '/tasks', label: '任务管理', icon: <SettingOutlined /> },
];

export function AppLayout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation();
  const selected = navigation.find((item) => item.end ? pathname === item.to : pathname.startsWith(item.to))?.to ?? '/';
  return <Layout className="app-shell ant-app-shell"><Sider className="sidebar" width={250} theme="dark"><div className="brand"><span className="brand-mark">A</span><span><Typography.Text strong>A-STOCK</Typography.Text><Typography.Text type="secondary" className="brand-subtitle">STRATEGY DESK</Typography.Text></span></div><Typography.Text type="secondary" className="sidebar-section-label">WORKSPACE</Typography.Text><Menu theme="dark" mode="inline" selectedKeys={[selected]} items={navigation.map((item) => ({ key: item.to, icon: item.icon, label: <NavLink to={item.to}>{item.label}</NavLink> }))} /><div className="sidebar-footer"><Space><Tag color="success">在线</Tag><Typography.Text type="secondary">数据服务</Typography.Text></Space><Typography.Text type="secondary">v0.1 / PREVIEW</Typography.Text></div></Sider><Layout className="main-content"><Header className="topbar"><Typography.Text type="secondary">INVESTMENT INTELLIGENCE <span className="topbar-separator">/</span> {pathname === '/' ? 'OVERVIEW' : pathname.slice(1).toUpperCase()}</Typography.Text><Typography.Text type="secondary">MARKET DESK <Typography.Text type="warning">·</Typography.Text> 2026.09.02</Typography.Text></Header><Content>{children}</Content></Layout></Layout>;
}
