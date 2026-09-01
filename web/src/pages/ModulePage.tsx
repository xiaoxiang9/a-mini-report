import { Card, Empty, Tag, Typography } from 'antd';

export function ModulePage({ title, kicker, description }: { title: string; kicker: string; description: string }) {
  return <div className="module-page page-wrap"><Typography.Text className="overline">{kicker}</Typography.Text><Typography.Title>{title}</Typography.Title><Typography.Paragraph className="module-intro">{description}</Typography.Paragraph><Card className="empty-module" bordered><Empty image={<span className="empty-icon">◌</span>} description={<><Typography.Text strong>功能正在构建中</Typography.Text><br /><Typography.Text type="secondary">数据接入后，这里将成为你的专属投研工作台。</Typography.Text></>} /><Tag color="gold">即将上线</Tag></Card></div>;
}
