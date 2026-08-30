const { fetchTrackedStocks, addTrackedStock, removeTrackedStock } = require('../../services/stocks.js');
Page({
  data: { stocks: [], code: '', loading: true, message: '' },
  onShow() { this.loadStocks(); },
  async loadStocks() { this.setData({ loading: true, message: '' }); try { this.setData({ stocks: await fetchTrackedStocks() }); } catch (error) { this.setData({ message: '列表加载失败，请检查 API 服务' }); } finally { this.setData({ loading: false }); } },
  onCodeInput(event) { this.setData({ code: event.detail.value }); },
  async onAdd() { if (!this.data.code.trim()) return this.setData({ message: '请输入股票代码' }); try { await addTrackedStock(this.data.code); this.setData({ code: '' }); this.loadStocks(); } catch (error) { this.setData({ message: error.message.includes('503') ? 'Tushare 暂不可用' : '添加失败，请检查股票代码' }); } },
  onDetail(event) { wx.navigateTo({ url: `/pages/stock-detail/stock-detail?tsCode=${encodeURIComponent(event.currentTarget.dataset.code)}` }); },
  onRemove(event) { const { code } = event.currentTarget.dataset; wx.showModal({ title: '移除追踪', content: `确认移除 ${code}？`, success: (result) => { if (result.confirm) removeTrackedStock(code).then(() => this.loadStocks()).catch(() => this.setData({ message: '移除失败' })); } }); },
});
