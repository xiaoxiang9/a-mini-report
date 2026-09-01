import { FormEvent, useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { addTrackedStock, fetchStockDetail, fetchTrackedStocks, removeTrackedStock, searchStocks, StockDetail, StockSearchResult } from '../api/stocks';
import { formatStockError, getSearchResultAction } from './stockSelector';

function Metric({ label, value }: { label: string; value: number | null }) {
  return <div className="stock-metric"><span>{label}</span><strong>{value == null ? '—' : value.toFixed(2)}</strong></div>;
}

export function StockTrackingPage() {
  const [stocks, setStocks] = useState<StockDetail[]>([]);
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<StockSearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [addingCode, setAddingCode] = useState<string | null>(null);
  const [message, setMessage] = useState('');
  const [modalMessage, setModalMessage] = useState('');
  const [suggestions, setSuggestions] = useState<StockSearchResult[]>([]);
  const [loading, setLoading] = useState(true);
  const load = () => fetchTrackedStocks().then(setStocks).catch(() => setMessage('列表加载失败，请检查 API 服务')).finally(() => setLoading(false));
  useEffect(() => { void load(); }, []);
  const search = async (event: FormEvent) => { event.preventDefault(); const keyword = query.trim(); if (!keyword) { setModalMessage('请输入股票名称或代码'); setResults([]); return; } setIsSearching(true); setModalMessage(''); try { setResults(await searchStocks(keyword)); } catch (error) { setResults([]); setModalMessage(formatStockError(error)); } finally { setIsSearching(false); } };
  const openAdd = () => { setIsAddOpen(true); setQuery(''); setResults([]); setMessage(''); setModalMessage(''); };
  const closeAdd = () => { if (addingCode) return; setIsAddOpen(false); };
  const addFromResult = async (item: StockSearchResult) => { if (item.isTracked || addingCode) return; setAddingCode(item.tsCode); setModalMessage(''); try { await addTrackedStock(item.tsCode); setModalMessage(`${item.stockName} 已添加`); setResults((current) => current.map((result) => result.tsCode === item.tsCode ? { ...result, isTracked: true } : result)); await load(); } catch (error) { setModalMessage(formatStockError(error)); } finally { setAddingCode(null); } };
  const remove = async (tsCode: string) => { if (!window.confirm(`确认移除 ${tsCode}？`)) return; await removeTrackedStock(tsCode); await load(); };
  return <div className="module-page page-wrap"><div className="module-heading"><div><p className="overline">STOCK TRACKING</p><h1>个股追踪</h1><p className="module-intro">持续跟踪关注标的，所有指标标注最新交易日。</p></div><button className="primary-button" onClick={openAdd}>新增</button></div>{message && <div className="notice">{message}</div>}{loading ? <div className="loading-bar">正在加载追踪列表…</div> : stocks.length === 0 ? <div className="empty-module"><span className="empty-icon">◌</span><strong>还没有追踪股票</strong><span>点击右上角“新增”，开始建立自己的观察清单。</span></div> : <div className="stock-list">{stocks.map((stock) => <article className="stock-row" key={stock.tsCode}><Link to={`/stock-tracking/${stock.tsCode}`}><div className="stock-name"><strong>{stock.stockName}</strong><span>{stock.tsCode}</span></div><Metric label="现价" value={stock.currentPrice} /><Metric label="7日涨幅" value={stock.change7dPercent} /><Metric label="PE" value={stock.peTtm} /><Metric label="PE历史百分位" value={stock.pePercentile} /><Metric label="PB" value={stock.pb} /><Metric label="PB历史百分位" value={stock.pbPercentile} /></Link><button className="text-button" onClick={() => void remove(stock.tsCode)}>移除</button></article>)}</div>}{isAddOpen && <div className="modal-backdrop" onClick={closeAdd}><section className="stock-modal" role="dialog" aria-modal="true" aria-labelledby="stock-modal-title" onClick={(event) => event.stopPropagation()}><div className="modal-header"><div><p className="overline">ADD STOCK</p><h2 id="stock-modal-title">新增追踪股票</h2></div><button className="modal-close" onClick={closeAdd} disabled={Boolean(addingCode)}>×</button></div><form className="modal-search" onSubmit={search}><input value={query} onChange={(event) => { setQuery(event.target.value); setModalMessage(''); }} placeholder="搜索股票名称或代码，如 贵州茅台 / 600519" autoFocus /><button type="submit" disabled={isSearching}>{isSearching ? '搜索中…' : '搜索'}</button></form>{modalMessage && <div className="modal-notice">{modalMessage}</div>}{isSearching ? <div className="modal-loading">正在搜索股票…</div> : results.length > 0 ? <div className="search-result-table"><div className="result-row result-head"><span>股票</span><span>代码</span><span>交易所</span><span>操作</span></div>{results.map((item) => { const action = getSearchResultAction(item.isTracked, addingCode === item.tsCode); return <div className="result-row" key={item.tsCode}><span><strong>{item.stockName}</strong></span><span>{item.tsCode}</span><span>{item.exchange}</span><button className="result-action" disabled={action.disabled} onClick={() => void addFromResult(item)}>{action.label}</button></div>; })}</div> : query.trim() ? <div className="modal-empty">暂无匹配股票</div> : <div className="modal-empty">输入股票名称或代码后点击搜索</div>}</section></div>}</div>;
}

export function StockDetailPage() {
  const { tsCode = '' } = useParams(); const navigate = useNavigate(); const [stock, setStock] = useState<StockDetail | null>(null); const [error, setError] = useState('');
  useEffect(() => { fetchStockDetail(tsCode).then(setStock).catch(() => setError('个股详情加载失败')); }, [tsCode]);
  if (error) return <div className="module-page page-wrap"><p className="notice">{error}</p><Link className="back-link" to="/stock-tracking">返回追踪列表</Link></div>;
  if (!stock) return <div className="module-page page-wrap"><div className="loading-bar">正在加载个股详情…</div></div>;
  return <div className="module-page page-wrap"><button className="back-link" onClick={() => navigate('/stock-tracking')}>← 返回追踪列表</button><p className="overline">STOCK DETAIL</p><h1>{stock.stockName}</h1><p className="module-intro">{stock.tsCode} · 最新交易日 {stock.latestTradeDate ?? '暂无'}</p><div className="stock-detail-grid"><Metric label="当前股价" value={stock.currentPrice} /><Metric label="最近7日涨幅" value={stock.change7dPercent} /><Metric label="PE-TTM" value={stock.peTtm} /><Metric label="PE历史百分位" value={stock.pePercentile} /><Metric label="PB" value={stock.pb} /><Metric label="PB历史百分位" value={stock.pbPercentile} /></div><p className="data-source">数据来源：{stock.dataSource ?? '暂无'} · 同步时间：{stock.lastSyncedAt ?? '暂无'}</p></div>;
}
