const { fetchStockDetail } = require('../../services/stocks.js');
Page({ data: { stock: null, message: '' }, onLoad(options) { this.setData({ tsCode: decodeURIComponent(options.tsCode || '') }); this.load(); }, async load() { try { this.setData({ stock: await fetchStockDetail(this.data.tsCode) }); } catch (error) { this.setData({ message: '个股详情加载失败' }); } } });
