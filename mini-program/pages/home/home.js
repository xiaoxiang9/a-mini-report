const { fetchHomeSummary, fallbackHomeSummary } = require('../../services/home.js');

Page({
  data: { loading: true, error: '', summary: fallbackHomeSummary },
  onLoad() { this.loadSummary(); },
  async loadSummary() {
    this.setData({ loading: true, error: '' });
    try {
      const summary = await fetchHomeSummary();
      this.setData({ summary, loading: false });
    } catch (_error) {
      this.setData({ summary: fallbackHomeSummary, loading: false, error: '暂时无法连接服务，当前显示基础内容' });
    }
  },
  retry() { this.loadSummary(); },
  openFeature(event) {
    const { key, status } = event.currentTarget.dataset;
    if (status !== 'available') return;
    const paths = { 'daily-review': '/pages/daily-review/daily-review' };
    if (paths[key]) wx.switchTab({ url: paths[key] });
  },
});
