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
  return <Layout className="app-shell ant-app-shell"><Sider className="sidebar" width={250} theme="light"><div className="brand"><span className="brand-mark">A</span><Typography.Text strong>A-STOCK</Typography.Text></div><Typography.Text type="secondary" className="sidebar-section-label">工作区</Typography.Text><Menu theme="light" mode="inline" selectedKeys={[selected]} items={navigation.map((item) => ({ key: item.to, icon: item.icon, label: <NavLink to={item.to}>{item.label}</NavLink> }))} /><div className="sidebar-footer"><Space><Tag color="success">在线</Tag><Typography.Text type="secondary">数据服务</Typography.Text></Space><Typography.Text type="secondary">版本 0.1</Typography.Text></div></Sider><Layout className="main-content"><Header className="topbar"><Typography.Text type="secondary">投资策略平台 <span className="topbar-separator">/</span> {pathname === '/' ? '总览' : navigation.find((item) => item.to !== '/' && pathname.startsWith(item.to))?.label ?? '页面'}</Typography.Text><Typography.Text type="secondary">市场数据 <Typography.Text type="warning">·</Typography.Text> 2026.09.02</Typography.Text></Header><Content>{children}</Content></Layout></Layout>;
}
