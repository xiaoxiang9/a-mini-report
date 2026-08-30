import { useEffect, useState } from 'react';
import { fetchHomeSummary } from '../api/home';
import { fallbackHomeSummary } from '../data/fallback';

export function OverviewPage() {
  const [summary, setSummary] = useState(fallbackHomeSummary);
  const [loading, setLoading] = useState(true);
  const [offline, setOffline] = useState(false);
  useEffect(() => { fetchHomeSummary().then(setSummary).catch(() => setOffline(true)).finally(() => setLoading(false)); }, []);
  return <div className="overview page-wrap">
    <section className="welcome-row"><div><p className="product-name">{summary.productName}</p><p className="overline">GOOD MORNING, INVESTOR</p><h1>读懂市场，<em>先人一步。</em></h1><p className="lead">让每一次复盘都有依据，让每一个策略都可追踪。</p></div><div className="market-chip"><span className="pulse"></span><span>MARKET WATCH</span><strong>{summary.statusText}</strong></div></section>
    {offline && <div className="notice">当前显示基础内容 · 数据服务暂时不可用</div>}
    {loading && <div className="loading-bar">正在同步平台状态…</div>}
    <section className="signal-panel"><div className="panel-caption"><span>PLATFORM SIGNAL</span><span>今日观察 / 01</span></div><div className="signal-body"><div><span className="signal-number">01</span><h2>{summary.tagline}</h2></div><p>从市场脉络到个股变化<br />建立一套属于你的投资观察系统。</p></div></section>
    <section className="modules"><div className="section-heading"><div><p className="overline">CORE MODULES</p><h2>你的投资工作台</h2></div><span>EXPLORE <b>→</b></span></div><div className="module-grid">{summary.features.map((feature, index) => <article className={`module-card ${feature.status === 'available' ? 'available' : 'coming'}`} key={feature.key}><div className="card-top"><span className="card-index">0{index + 1}</span><span className="card-status">{feature.status === 'available' ? 'AVAILABLE' : 'COMING SOON'}</span></div><div className="card-glyph">{['⌁', '◎', '◌'][index]}</div><h3>{feature.title}</h3><p>{feature.description}</p><a href={feature.status === 'available' ? '/daily-review' : '#'} onClick={(event) => feature.status !== 'available' && event.preventDefault()}>{feature.status === 'available' ? '进入模块 →' : '即将上线'}</a></article>)}</div></section>
  </div>;
}
