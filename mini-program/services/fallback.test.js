const test = require('node:test');
const assert = require('node:assert/strict');
const { fallbackHomeSummary } = require('./fallback.js');

test('fallback contains three unique features and no market metrics', () => {
  assert.equal(fallbackHomeSummary.productName, 'A股投资策略平台');
  assert.equal(fallbackHomeSummary.features.length, 3);
  assert.equal(new Set(fallbackHomeSummary.features.map((feature) => feature.key)).size, 3);
  assert.equal(Object.hasOwn(fallbackHomeSummary, 'price'), false);
  assert.equal(Object.hasOwn(fallbackHomeSummary, 'percentage'), false);
});
