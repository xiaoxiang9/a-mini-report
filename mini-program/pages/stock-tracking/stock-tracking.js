const { fetchTrackedStocks, addTrackedStock, removeTrackedStock, searchStocks } = require('../../services/stocks.js');
Page({
  data: { stocks: [], code: '', selectedStock: null, suggestions: [], loading: true, message: '' },
  onShow() { this.loadStocks(); },
  async loadStocks() { this.setData({ loading: true, message: '' }); try { this.setData({ stocks: await fetchTrackedStocks() }); } catch (error) { this.setData({ message: '列表加载失败，请检查 API 服务' }); } finally { this.setData({ loading: false }); } },
  onCodeInput(event) { const code = event.detail.value; this.setData({ code, selectedStock: null, message: '' }); clearTimeout(this.searchTimer); if (!code.trim()) return this.setData({ suggestions: [] }); this.searchTimer = setTimeout(() => searchStocks(code.trim()).then((suggestions) => this.setData({ suggestions })).catch(() => this.setData({ suggestions: [] })), 300); },
  selectSuggestion(event) { const item = event.currentTarget.dataset.item; if (item.isTracked) return this.setData({ message: '该股票已在追踪列表中' }); this.setData({ code: `${item.stockName} · ${item.tsCode}`, selectedStock: item, suggestions: [], message: '' }); },
  async onAdd() { if (!this.data.selectedStock) return this.setData({ message: '请先选择搜索结果' }); try { await addTrackedStock(this.data.selectedStock.tsCode); this.setData({ code: '', selectedStock: null, suggestions: [] }); this.loadStocks(); } catch (error) { this.setData({ message: error.message.includes('503') ? 'Tushare 暂不可用' : '添加股票失败，请稍后重试' }); } },
  onDetail(event) { wx.navigateTo({ url: `/pages/stock-detail/stock-detail?tsCode=${encodeURIComponent(event.currentTarget.dataset.code)}` }); },
  onRemove(event) { const { code } = event.currentTarget.dataset; wx.showModal({ title: '移除追踪', content: `确认移除 ${code}？`, success: (result) => { if (result.confirm) removeTrackedStock(code).then(() => this.loadStocks()).catch(() => this.setData({ message: '移除失败' })); } }); },
});
