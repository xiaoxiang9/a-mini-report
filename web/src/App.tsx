import { Route, Routes } from 'react-router-dom';
import { AppLayout } from './layout/AppLayout';
import { ModulePage } from './pages/ModulePage';
import { OverviewPage } from './pages/OverviewPage';
import { StockDetailPage, StockTrackingPage } from './pages/StockTrackingPage';
import { TaskManagementPage } from './pages/TaskManagementPage';

export function App() {
  return <AppLayout><Routes><Route path="/" element={<OverviewPage />} /><Route path="/daily-review" element={<ModulePage title="每日复盘" kicker="DAILY REVIEW" description="梳理市场脉络，捕捉关键变化。" />} /><Route path="/stock-tracking" element={<StockTrackingPage />} /><Route path="/stock-tracking/:tsCode" element={<StockDetailPage />} /><Route path="/strategy-selection" element={<ModulePage title="策略选股" kicker="STRATEGY SELECTION" description="用规则筛选潜在机会，构建可复用策略。" />} /><Route path="/tasks" element={<TaskManagementPage />} /></Routes></AppLayout>;
}
