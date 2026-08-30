# 双前端改造 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有微信小程序、DDD API 和 MySQL 基础上新增可独立运行的 React Web 前端，并让腾讯云 Nginx 同时托管 Web 和 API。

**Architecture:** `mini-program/` 和 `web/` 是两个独立前端，仅共享 HTTPS API 字段约定。Nginx 将 `/` 指向 Web 静态目录，将 `/api/` 反向代理到 Docker 中的 Fastify 服务。

**Tech Stack:** React 19、Vite、TypeScript、React Router、Vitest、Fastify、Prisma、MySQL、Nginx。

## Global Constraints

- Web 与微信小程序不共享页面源码，只共享 API DTO 字段。
- Web 生产 API 基地址为 `https://myxiang.online`。
- 第一阶段不接入真实行情、交易接口或虚构金融数值。
- 未实现业务能力显示“即将上线”。
- 敏感配置不提交，Web 使用 `VITE_API_BASE_URL`。

## 文件结构

- `web/package.json`、`web/tsconfig*.json`、`web/vite.config.ts`：Web 工程和脚本。
- `web/src/api/`：首页摘要请求。
- `web/src/data/`：API 失败兜底数据。
- `web/src/layout/`：侧边栏和桌面布局。
- `web/src/pages/`：总览与三个业务模块页面。
- `web/src/routes/`：路由配置。
- `web/src/styles/`：全局设计变量。
- `deploy/nginx/myxiang.online.conf`：版本化 Nginx 配置模板。
- `.github/workflows/deploy.yml`：构建并上传 Web 静态文件。

### Task 1: 初始化 Web 工程与 API 契约

**Files:**
- Create: `web/package.json`
- Create: `web/tsconfig.json`
- Create: `web/tsconfig.node.json`
- Create: `web/vite.config.ts`
- Create: `web/index.html`
- Create: `web/src/api/home.ts`
- Create: `web/src/data/fallback.ts`
- Create: `web/src/api/home.test.ts`

- [ ] **Step 1: Write the failing API mapping test**

测试 `normalizeHomeSummary()` 能保留 productName、tagline、statusText，并将 features 映射为 Web 需要的结构；缺字段时抛出可识别错误。

- [ ] **Step 2: Run the test and verify it fails**

Run: `cd web && npm test -- --run src/api/home.test.ts`
Expected: FAIL because the Web package and normalizer do not exist.

- [ ] **Step 3: Implement the Web package, API client and fallback**

`fetchHomeSummary()` 使用 `import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:3000'`，请求 `/api/home/summary`；失败由页面捕获并使用 `fallbackHomeSummary`。

- [ ] **Step 4: Run test, typecheck and build**

Run: `cd web && npm test -- --run && npm run typecheck && npm run build`
Expected: tests pass, typecheck and build exit 0.

### Task 2: Implement Web layout, routes and pages

**Files:**
- Create: `web/src/main.tsx`
- Create: `web/src/App.tsx`
- Create: `web/src/layout/AppLayout.tsx`
- Create: `web/src/layout/AppLayout.test.tsx`
- Create: `web/src/pages/OverviewPage.tsx`
- Create: `web/src/pages/ModulePage.tsx`
- Create: `web/src/styles/global.css`

- [ ] **Step 1: Write the failing layout test**

验证渲染 Web 应用时出现“A股投资策略平台”“每日复盘”“个股追踪”“策略选股”，并存在“即将上线”状态文案。

- [ ] **Step 2: Run the test and verify it fails**

Run: `cd web && npm test -- --run src/layout/AppLayout.test.tsx`
Expected: FAIL because the React application does not exist.

- [ ] **Step 3: Implement routes and desktop layout**

使用 React Router 配置 `/`、`/daily-review`、`/stock-tracking`、`/strategy-selection`；总览请求 API 并处理 loading/error/fallback；侧边栏导航使用 `NavLink`。

- [ ] **Step 4: Run tests and build**

Run: `cd web && npm test -- --run && npm run build`
Expected: all tests pass and `web/dist/index.html` exists.

### Task 3: Integrate production static hosting and GitHub deployment

**Files:**
- Modify: `docker-compose.prod.yml`
- Modify: `.github/workflows/deploy.yml`
- Create: `deploy/nginx/myxiang.online.conf`
- Modify: `README.md`

- [ ] **Step 1: Add Web build to deployment workflow**

GitHub Actions 在上传前执行 `cd web && npm ci && npm run build`，再将 `web/dist` 上传到 `/opt/a-mini-report/web/dist`。

- [ ] **Step 2: Add Nginx configuration template**

配置 `root /opt/a-mini-report/web/dist`、SPA `try_files $uri $uri/ /index.html`，并保留 `/api/` 到 `127.0.0.1:3000` 的代理和 HTTPS 证书路径。

- [ ] **Step 3: Update README deployment instructions**

记录 Web 构建、Nginx 配置、GitHub Secrets 和健康检查命令。

- [ ] **Step 4: Run workflow/config checks locally**

Run: `cd web && npm run build`; then `git diff --check` and `git status --short`.
Expected: build succeeds and no whitespace errors.

### Task 4: Deploy and verify on Tencent Cloud

- [ ] **Step 1: Commit and push the dual-frontend change**

Run: `git add web deploy .github README.md docker-compose.prod.yml && git commit -m "feat: add web frontend" && git push origin main`.

- [ ] **Step 2: Upload Web dist and Nginx config to the authorized server**

Use the existing SSH key; preserve `/opt/a-mini-report/.env` and MySQL volume.

- [ ] **Step 3: Validate Nginx and reload the actual BaoTa master process**

Run remotely: `nginx -t`, then `kill -HUP $(cat /www/server/nginx/logs/nginx.pid)`.

- [ ] **Step 4: Verify public Web and APIs**

Run: `curl -fsS https://myxiang.online/`, `curl -fsS https://myxiang.online/api/health`, and `curl -fsS https://myxiang.online/api/home/summary`.
Expected: Web returns HTML, health returns database `up`, summary returns three feature entries.

