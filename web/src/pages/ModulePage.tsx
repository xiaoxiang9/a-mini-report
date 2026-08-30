export function ModulePage({ title, kicker, description }: { title: string; kicker: string; description: string }) {
  return <div className="module-page page-wrap"><p className="overline">{kicker}</p><h1>{title}</h1><p className="module-intro">{description}</p><div className="empty-module"><span className="empty-icon">◌</span><strong>功能正在构建中</strong><span>数据接入后，这里将成为你的专属投研工作台。</span><label>COMING SOON</label></div></div>;
}
