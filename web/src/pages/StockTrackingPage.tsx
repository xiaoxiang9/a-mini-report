import { FormEvent, useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { addTrackedStock, fetchStockDetail, fetchTrackedStocks, removeTrackedStock, StockDetail } from '../api/stocks';

function Metric({ label, value }: { label: string; value: number | null }) {
  return <div className="stock-metric"><span>{label}</span><strong>{value == null ? '—' : value.toFixed(2)}</strong></div>;
}

export function StockTrackingPage() {
  const [stocks, setStocks] = useState<StockDetail[]>([]);
  const [code, setCode] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const load = () => fetchTrackedStocks().then(setStocks).catch(() => setMessage('列表加载失败，请检查 API 服务')).finally(() => setLoading(false));
  useEffect(() => { void load(); }, []);
  const submit = async (event: FormEvent) => {
    event.preventDefault(); setMessage('');
    try { await addTrackedStock(code); setCode(''); await load(); } catch (error) { setMessage(error instanceof Error && error.message.includes('503') ? 'Tushare 暂不可用，请稍后重试' : '添加失败，请输入标准股票代码'); }
  };
  const remove = async (tsCode: string) => { if (!window.confirm(`确认移除 ${tsCode}？`)) return; await removeTrackedStock(tsCode); await load(); };
  return <div className="module-page page-wrap"><p className="overline">STOCK TRACKING</p><h1>个股追踪</h1><p className="module-intro">持续跟踪关注标的，所有指标标注最新交易日。</p><form className="stock-add-form" onSubmit={submit}><input value={code} onChange={(event) => setCode(event.target.value)} placeholder="输入股票代码，如 600519.SH" /><button type="submit">添加股票</button></form>{message && <div className="notice">{message}</div>}{loading ? <div className="loading-bar">正在加载追踪列表…</div> : stocks.length === 0 ? <div className="empty-module"><span className="empty-icon">◌</span><strong>还没有追踪股票</strong><span>添加一只股票，开始建立自己的观察清单。</span></div> : <div className="stock-list">{stocks.map((stock) => <article className="stock-row" key={stock.tsCode}><Link to={`/stock-tracking/${stock.tsCode}`}><div className="stock-name"><strong>{stock.stockName}</strong><span>{stock.tsCode}</span></div><Metric label="现价" value={stock.currentPrice} /><Metric label="7日涨幅" value={stock.change7dPercent} /><Metric label="PE" value={stock.peTtm} /><Metric label="PE历史百分位" value={stock.pePercentile} /><Metric label="PB" value={stock.pb} /><Metric label="PB历史百分位" value={stock.pbPercentile} /></Link><button className="text-button" onClick={() => void remove(stock.tsCode)}>移除</button></article>)}</div>}</div>;
}

export function StockDetailPage() {
  const { tsCode = '' } = useParams(); const navigate = useNavigate(); const [stock, setStock] = useState<StockDetail | null>(null); const [error, setError] = useState('');
  useEffect(() => { fetchStockDetail(tsCode).then(setStock).catch(() => setError('个股详情加载失败')); }, [tsCode]);
  if (error) return <div className="module-page page-wrap"><p className="notice">{error}</p><Link className="back-link" to="/stock-tracking">返回追踪列表</Link></div>;
  if (!stock) return <div className="module-page page-wrap"><div className="loading-bar">正在加载个股详情…</div></div>;
  return <div className="module-page page-wrap"><button className="back-link" onClick={() => navigate('/stock-tracking')}>← 返回追踪列表</button><p className="overline">STOCK DETAIL</p><h1>{stock.stockName}</h1><p className="module-intro">{stock.tsCode} · 最新交易日 {stock.latestTradeDate ?? '暂无'}</p><div className="stock-detail-grid"><Metric label="当前股价" value={stock.currentPrice} /><Metric label="最近7日涨幅" value={stock.change7dPercent} /><Metric label="PE-TTM" value={stock.peTtm} /><Metric label="PE历史百分位" value={stock.pePercentile} /><Metric label="PB" value={stock.pb} /><Metric label="PB历史百分位" value={stock.pbPercentile} /></div><p className="data-source">数据来源：{stock.dataSource ?? '暂无'} · 同步时间：{stock.lastSyncedAt ?? '暂无'}</p></div>;
}
