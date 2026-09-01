const { fetchTrackedStocks, addTrackedStock, removeTrackedStock, searchStocks } = require('../../services/stocks.js');
Page({
  data: { stocks: [], addOpen: false, query: '', results: [], searched: false, searching: false, addingCode: '', loading: true, message: '' },
  onShow() { this.loadStocks(); },
  async loadStocks() { this.setData({ loading: true, message: '' }); try { this.setData({ stocks: await fetchTrackedStocks() }); } catch (error) { this.setData({ message: '列表加载失败，请检查 API 服务' }); } finally { this.setData({ loading: false }); } },
  openAdd() { this.setData({ addOpen: true, query: '', results: [], searched: false, message: '' }); },
  closeAdd() { if (!this.data.addingCode) this.setData({ addOpen: false }); },
  stopPropagation() {},
  onQueryInput(event) { this.setData({ query: event.detail.value, searched: false, results: [] }); },
  async search() { const query = this.data.query.trim(); if (!query) return this.setData({ message: '请输入股票名称或代码' }); this.setData({ searching: true, message: '' }); try { this.setData({ results: await searchStocks(query), searched: true }); } catch (error) { this.setData({ results: [], searched: true, message: '搜索失败，请稍后重试' }); } finally { this.setData({ searching: false }); } },
  async addResult(event) { const item = event.currentTarget.dataset.item; if (item.isTracked || this.data.addingCode) return; this.setData({ addingCode: item.tsCode, message: '' }); try { await addTrackedStock(item.tsCode); this.setData({ results: this.data.results.map((result) => result.tsCode === item.tsCode ? { ...result, isTracked: true } : result), message: `${item.stockName} 已添加` }); await this.loadStocks(); } catch (error) { this.setData({ message: error.message.includes('503') ? 'Tushare 暂不可用' : '添加股票失败，请稍后重试' }); } finally { this.setData({ addingCode: '' }); } },
  onDetail(event) { wx.navigateTo({ url: `/pages/stock-detail/stock-detail?tsCode=${encodeURIComponent(event.currentTarget.dataset.code)}` }); },
  onRemove(event) { const { code } = event.currentTarget.dataset; wx.showModal({ title: '移除追踪', content: `确认移除 ${code}？`, success: (result) => { if (result.confirm) removeTrackedStock(code).then(() => this.loadStocks()).catch(() => this.setData({ message: '移除失败' })); } }); },
});
