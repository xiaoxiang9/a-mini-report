function request(path, options = {}) {
  const app = getApp();
  return new Promise((resolve, reject) => wx.request({ url: `${app.globalData.apiBaseUrl}${path}`, ...options, success(response) { if (response.statusCode >= 200 && response.statusCode < 300) return resolve(response.data); reject(new Error(`STOCK_API_HTTP_${response.statusCode}`)); }, fail: reject }));
}
function fetchTrackedStocks() { return request('/api/stocks/tracking'); }
function fetchStockDetail(tsCode) { return request(`/api/stocks/${encodeURIComponent(tsCode)}`); }
function addTrackedStock(tsCode) { return request('/api/stocks/tracking', { method: 'POST', data: { tsCode }, header: { 'content-type': 'application/json' } }); }
function removeTrackedStock(tsCode) { return request(`/api/stocks/${encodeURIComponent(tsCode)}`, { method: 'DELETE' }); }
module.exports = { fetchTrackedStocks, fetchStockDetail, addTrackedStock, removeTrackedStock };
