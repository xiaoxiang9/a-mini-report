# 个股搜索下拉选择 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将个股追踪的搜索框改为必须先选择候选股票、再点击添加的下拉选择控件。

**Architecture:** 复用现有股票搜索 API。Web 端增加 `selectedStock` 状态，小程序增加 `selectedStock` 页面数据；输入变化清除选中项，候选点击只选中，提交时只使用选中股票的 `tsCode`。

**Tech Stack:** React、TypeScript、Vitest、原生微信小程序、现有 FastAPI 股票 API。

## Global Constraints

- 不修改后端接口和数据库结构。
- Web 与微信小程序交互规则保持一致。
- 用户未选中候选项时不得调用添加股票接口。
- 用户再次编辑搜索文本时必须清除之前的选中项。

---

### Task 1: Web 下拉选择行为

**Files:**
- Modify: `web/src/pages/StockTrackingPage.tsx`
- Modify: `web/src/pages/StockTrackingPage.test.tsx` (create if absent)

**Interfaces:**
- Consumes: `searchStocks(query)`, `addTrackedStock(tsCode)`。
- Produces: 候选点击只更新选中状态；表单提交只接受 `selectedStock.tsCode`。

- [ ] **Step 1: Write the failing test**

在 `web/src/pages/StockTrackingPage.test.tsx` 中覆盖：输入后显示候选项；点击候选项不调用添加；随后点击添加才提交候选股票代码；直接提交未选中内容不调用添加。

- [ ] **Step 2: Run the test to verify it fails**

Run: `npm test -- src/pages/StockTrackingPage.test.tsx`

Expected: FAIL，因为当前候选项点击会直接添加，且表单允许直接提交输入文本。

- [ ] **Step 3: Write minimal implementation**

增加 `selectedStock` 状态；输入变化时设置为 `null`；`selectSuggestion` 只设置选中项；`submit` 在没有选中项时显示提示，否则调用 `addTrackedStock(selectedStock.tsCode)`；添加按钮使用 `disabled={!selectedStock}`。

- [ ] **Step 4: Run the test to verify it passes**

Run: `npm test -- src/pages/StockTrackingPage.test.tsx`

Expected: PASS。

- [ ] **Step 5: Commit**

```bash
git add web/src/pages/StockTrackingPage.tsx web/src/pages/StockTrackingPage.test.tsx
git commit -m "feat: require stock selection before tracking"
```

### Task 2: 微信小程序同步交互

**Files:**
- Modify: `mini-program/pages/stock-tracking/stock-tracking.js`
- Modify: `mini-program/pages/stock-tracking/stock-tracking.wxml`

**Interfaces:**
- Consumes: `searchStocks(query)`, `addTrackedStock(tsCode)`。
- Produces: 页面数据 `selectedStock`，与 Web 端一致的选择后提交流程。

- [ ] **Step 1: Write the failing test/check**

确认页面逻辑中存在“输入清除选中项、候选点击不调用添加、提交使用 selectedStock.tsCode”的行为检查清单，并以静态检查命令验证关键代码尚不存在。

- [ ] **Step 2: Run the check to verify it fails**

Run: `rg -n "selectedStock|addTrackedStock\(this\.data\.code" mini-program/pages/stock-tracking/stock-tracking.js`

Expected: 当前没有 `selectedStock`，且 `onAdd` 使用输入框文本。

- [ ] **Step 3: Write minimal implementation**

在 `data` 增加 `selectedStock: null`；`onCodeInput` 清除选中项；`selectSuggestion` 只设置 `selectedStock` 和展示值；`onAdd` 仅在选中项存在时提交其 `tsCode`；WXML 按选中状态禁用添加按钮并展示已选标的。

- [ ] **Step 4: Run the check to verify it passes**

Run: `rg -n "selectedStock|addTrackedStock\(this\.data\.selectedStock\.tsCode\)" mini-program/pages/stock-tracking/stock-tracking.js`

Expected: 命中选中状态和代码提交路径。

- [ ] **Step 5: Commit**

```bash
git add mini-program/pages/stock-tracking/stock-tracking.js mini-program/pages/stock-tracking/stock-tracking.wxml
git commit -m "feat: align mini program stock selector"
```

### Task 3: 全量验证与生产构建

**Files:**
- Verify: `web/src/api/stocks.test.ts`
- Verify: `web/src/pages/StockTrackingPage.test.tsx`

- [ ] **Step 1: Run Web tests**

Run: `npm test`

Expected: all test files pass。

- [ ] **Step 2: Build production Web**

Run: `VITE_API_BASE_URL=/ npm run build`

Expected: Vite build succeeds and `web/dist/index.html` is generated。

- [ ] **Step 3: Check the final diff**

Run: `git diff --check && git status --short`

Expected: no whitespace errors；仅包含本功能文件或已提交后的干净工作区。
