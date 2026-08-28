const { fallbackHomeSummary } = require('./fallback.js');

function fetchHomeSummary() {
  const app = getApp();
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/api/home/summary`,
      method: 'GET',
      success(response) {
        if (response.statusCode >= 200 && response.statusCode < 300) return resolve(response.data);
        reject(new Error(`HTTP_${response.statusCode}`));
      },
      fail: reject,
    });
  });
}

module.exports = { fetchHomeSummary, fallbackHomeSummary };
