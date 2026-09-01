const { fetchTrackedStocks, addTrackedStock, removeTrackedStock, searchStocks } = require('../../services/stocks.js');
Page({
  data: { stocks: [], addOpen: false, query: '', results: [], searched: false, searching: false, addingCode: '', loading: true, message: '', modalMessage: '' },
  onShow() { this.loadStocks(); },
  async loadStocks() { this.setData({ loading: true, message: '' }); try { this.setData({ stocks: await fetchTrackedStocks() }); } catch (error) { this.setData({ message: '列表加载失败，请检查 API 服务' }); } finally { this.setData({ loading: false }); } },
  openAdd() { this.setData({ addOpen: true, query: '', results: [], searched: false, message: '', modalMessage: '' }); },
  closeAdd() { if (!this.data.addingCode) this.setData({ addOpen: false }); },
  stopPropagation() {},
  onQueryInput(event) { this.setData({ query: event.detail.value, searched: false, results: [] }); },
  async search() { const query = this.data.query.trim(); if (!query) return this.setData({ modalMessage: '请输入股票名称或代码' }); this.setData({ searching: true, modalMessage: '' }); try { this.setData({ results: await searchStocks(query), searched: true }); } catch (error) { this.setData({ results: [], searched: true, modalMessage: this.formatStockError(error) }); } finally { this.setData({ searching: false }); } },
  formatStockError(error) { const message = error && error.message ? error.message : ''; if (message.includes('404') || message.includes('STOCK_NOT_FOUND')) return '未找到这支股票，请检查名称或代码'; if (message.includes('422') || message.includes('INVALID_TS_CODE')) return '股票代码格式不正确，请重新搜索并选择结果'; if (message.includes('503') || message.includes('TUSHARE_')) return '行情数据源暂不可用，请检查 Tushare 配置'; if (message.includes('fail') || message.includes('Network')) return '网络连接失败，请检查网络后重试'; return '操作失败，请稍后重试'; },
  async addResult(event) { const item = event.currentTarget.dataset.item; if (item.isTracked || this.data.addingCode) return; this.setData({ addingCode: item.tsCode, modalMessage: '' }); try { await addTrackedStock(item.tsCode); this.setData({ results: this.data.results.map((result) => result.tsCode === item.tsCode ? { ...result, isTracked: true } : result), modalMessage: `${item.stockName} 已添加` }); await this.loadStocks(); } catch (error) { this.setData({ modalMessage: this.formatStockError(error) }); } finally { this.setData({ addingCode: '' }); } },
  onDetail(event) { wx.navigateTo({ url: `/pages/stock-detail/stock-detail?tsCode=${encodeURIComponent(event.currentTarget.dataset.code)}` }); },
  onRemove(event) { const { code } = event.currentTarget.dataset; wx.showModal({ title: '移除追踪', content: `确认移除 ${code}？`, success: (result) => { if (result.confirm) removeTrackedStock(code).then(() => this.loadStocks()).catch(() => this.setData({ message: '移除失败' })); } }); },
});
