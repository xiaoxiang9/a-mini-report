# A股投资策略平台 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 初始化一个可运行的微信原生小程序和 Node.js/TypeScript DDD 后端，并通过 MySQL 提供欢迎页摘要。

**Architecture:** 前端位于 `mini-program/`，只通过 HTTP 调用后端；后端位于 `server/`，按 interfaces/application/domain/infrastructure 分层。Prisma 负责 MySQL 持久化，首页摘要由应用服务通过仓储端口读取。

**Tech Stack:** 微信原生小程序、Node.js、TypeScript、Fastify、Vitest、Prisma、MySQL、Docker Compose。

## Global Constraints

- 前端不得直接连接 MySQL，只调用 `/api` HTTP 接口。
- 领域层不得依赖 Fastify、Prisma 或微信运行时。
- 第一阶段不接入真实行情、财务数据、研报或交易接口。
- 页面不得伪造真实行情数字；未实现能力显示“即将上线”。
- 所有新行为先写失败测试，再写最小实现。
- 敏感配置只放在本地 `.env`，提交 `.env.example`，不提交真实密钥。

## 文件结构

将创建以下边界清晰的文件：

- `mini-program/`：微信小程序页面、Tab 配置、API 客户端和本地兜底内容。
- `server/src/interfaces/http/`：Fastify 路由与 DTO。
- `server/src/application/`：首页摘要和健康检查用例。
- `server/src/domain/`：三大业务域及共享领域类型、仓储接口。
- `server/src/infrastructure/`：Prisma Client、MySQL 仓储、配置和应用装配。
- `server/prisma/`：Schema 和种子数据。
- `docker-compose.yml`：本地 MySQL。
- `README.md`：启动和验收说明。

### Task 1: 建立后端工程与领域契约

**Files:**
- Create: `server/package.json`
- Create: `server/tsconfig.json`
- Create: `server/vitest.config.ts`
- Create: `server/src/domain/shared/feature.ts`
- Create: `server/src/domain/platform/home-summary.ts`
- Create: `server/src/domain/platform/home-summary-repository.ts`
- Create: `server/src/application/home/get-home-summary.ts`
- Create: `server/src/application/home/get-home-summary.test.ts`

**Interfaces:**
- `FeatureStatus = 'available' | 'coming-soon'`
- `FeatureEntry { key: string; title: string; description: string; status: FeatureStatus }`
- `HomeSummary { productName: string; tagline: string; statusText: string; features: FeatureEntry[] }`
- `HomeSummaryRepository.find(): Promise<HomeSummary>`
- `GetHomeSummary.execute(): Promise<HomeSummary>`

- [ ] **Step 1: Write the failing application test**

```ts
import { describe, expect, it } from 'vitest';
import { GetHomeSummary } from './get-home-summary';
import type { HomeSummaryRepository } from '../../domain/platform/home-summary-repository';

describe('GetHomeSummary', () => {
  it('returns the home summary provided by the repository', async () => {
    const summary = { productName: 'A股投资策略平台', tagline: '用数据，看清每一次市场波动', statusText: '今日市场，保持观察', features: [] };
    const repository: HomeSummaryRepository = { find: async () => summary };
    await expect(new GetHomeSummary(repository).execute()).resolves.toEqual(summary);
  });
});
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `cd server && npm test -- --run src/application/home/get-home-summary.test.ts`
Expected: FAIL because `GetHomeSummary` and its contract do not exist.

- [ ] **Step 3: Implement the domain types and application service**

`GetHomeSummary.execute()` only delegates to `HomeSummaryRepository.find()` and returns its result. Keep all types free of framework imports.

- [ ] **Step 4: Run the test and verify it passes**

Run: `cd server && npm test -- --run src/application/home/get-home-summary.test.ts`
Expected: 1 test passed.

### Task 2: Add Prisma/MySQL persistence and health infrastructure

**Files:**
- Create: `docker-compose.yml`
- Create: `server/.env.example`
- Create: `server/prisma/schema.prisma`
- Create: `server/prisma/seed.ts`
- Create: `server/src/infrastructure/config/env.ts`
- Create: `server/src/infrastructure/database/prisma.ts`
- Create: `server/src/infrastructure/platform/prisma-home-summary-repository.ts`
- Create: `server/src/infrastructure/platform/prisma-home-summary-repository.test.ts`
- Create: `server/src/infrastructure/database/health-check.ts`
- Modify: `server/package.json`

**Interfaces:**
- `PrismaHomeSummaryRepository.find(): Promise<HomeSummary>` reads `PlatformConfig` and ordered `FeatureEntry` records.
- `checkDatabase(prisma): Promise<'up' | 'down'>` runs a trivial database query and never exposes credentials.

- [ ] **Step 1: Add the Prisma schema and seed model**

Create `PlatformConfig(id, productName, tagline, statusText)` and `FeatureEntry(id, key, title, description, status, sortOrder)` with a unique feature key and an index on `sortOrder`.

- [ ] **Step 2: Add the MySQL container and environment template**

Configure MySQL 8 with database `a_stock_platform`, user `app`, and a non-production development password. The server reads `DATABASE_URL`, `PORT`, and `MINI_PROGRAM_API_BASE_URL`.

- [ ] **Step 3: Write the repository mapping test**

Test that a Prisma-shaped result maps to the exact `HomeSummary` DTO, including feature ordering and `status` values. Use a small in-memory Prisma-compatible stub; do not require MySQL for this unit test.

- [ ] **Step 4: Run the test and verify it fails**

Run: `cd server && npm test -- --run src/infrastructure/platform/prisma-home-summary-repository.test.ts`
Expected: FAIL because the repository mapper is missing.

- [ ] **Step 5: Implement the repository, Prisma client, seed, and health check**

Use Prisma `findFirst` plus ordered feature query or an equivalent relation query; map database records to domain types and keep Prisma types inside infrastructure.

- [ ] **Step 6: Run unit tests and type-check**

Run: `cd server && npm test -- --run && npm run typecheck`
Expected: all tests pass and TypeScript exits with code 0.

### Task 3: Expose Fastify HTTP APIs and application composition

**Files:**
- Create: `server/src/interfaces/http/routes/home.ts`
- Create: `server/src/interfaces/http/routes/health.ts`
- Create: `server/src/interfaces/http/app.ts`
- Create: `server/src/main.ts`
- Create: `server/src/interfaces/http/routes/home.test.ts`
- Modify: `server/package.json`

**Interfaces:**
- `GET /api/home/summary` returns `HomeSummary` with HTTP 200.
- `GET /api/health` returns `{ status: 'ok' | 'degraded', database: 'up' | 'down' }` and HTTP 200/503 accordingly.
- `buildApp(dependencies)` returns a Fastify instance suitable for injection tests.

- [ ] **Step 1: Write failing route tests**

Cover HTTP 200 and the exact JSON shape for `/api/home/summary`, plus HTTP 503 when the injected database health check returns `down`.

- [ ] **Step 2: Run the route tests and verify failure**

Run: `cd server && npm test -- --run src/interfaces/http/routes/home.test.ts`
Expected: FAIL because the Fastify app and routes do not exist.

- [ ] **Step 3: Implement routes and dependency composition**

Register routes under `/api`, inject `GetHomeSummary`, `HomeSummaryRepository`, and the health checker, and map unexpected errors to `{ error: 'INTERNAL_SERVER_ERROR' }` without leaking stack traces.

- [ ] **Step 4: Run route tests and verify pass**

Run: `cd server && npm test -- --run src/interfaces/http/routes/home.test.ts`
Expected: all route tests pass.

- [ ] **Step 5: Add start, migration, seed, and typecheck scripts**

Run: `cd server && npm run typecheck`
Expected: exit code 0.

### Task 4: Build the native mini-program welcome page

**Files:**
- Create: `mini-program/app.json`
- Create: `mini-program/app.js`
- Create: `mini-program/app.wxss`
- Create: `mini-program/pages/home/home.json`
- Create: `mini-program/pages/home/home.js`
- Create: `mini-program/pages/home/home.wxml`
- Create: `mini-program/pages/home/home.wxss`
- Create: `mini-program/pages/daily-review/daily-review.json`
- Create: `mini-program/pages/daily-review/daily-review.js`
- Create: `mini-program/pages/daily-review/daily-review.wxml`
- Create: `mini-program/pages/daily-review/daily-review.wxss`
- Create: `mini-program/pages/stock-tracking/stock-tracking.json`
- Create: `mini-program/pages/stock-tracking/stock-tracking.js`
- Create: `mini-program/pages/stock-tracking/stock-tracking.wxml`
- Create: `mini-program/pages/stock-tracking/stock-tracking.wxss`
- Create: `mini-program/pages/strategy-selection/strategy-selection.json`
- Create: `mini-program/pages/strategy-selection/strategy-selection.js`
- Create: `mini-program/pages/strategy-selection/strategy-selection.wxml`
- Create: `mini-program/pages/strategy-selection/strategy-selection.wxss`
- Create: `mini-program/services/home.js`
- Create: `mini-program/services/fallback.js`
- Create: `mini-program/services/fallback.test.js`

**Interfaces:**
- `services/home.js` exports `fetchHomeSummary(): Promise<HomeSummary>` using `wx.request` and `app.globalData.apiBaseUrl`.
- Home page state contains `loading`, `error`, `summary`, and `retry()`.
- Tab bar labels are exactly “每日复盘 / 个股追踪 / 策略选股”.

- [ ] **Step 1: Add page configuration and fallback content**

Create the three tab pages with explicit “即将上线” copy. Fallback summary must use the same DTO keys as the API and must not contain market numeric claims.

- [ ] **Step 2: Write a lightweight contract test for fallback data**

Assert the fallback has the product name, three unique feature keys, and no numeric price/percentage fields.

- [ ] **Step 3: Run the contract test and verify it fails**

Run: `node --test mini-program/services/fallback.test.js`
Expected: FAIL because fallback content is missing.

- [ ] **Step 4: Implement API client, home page, styles, and fallback**

Render loading, success, and failure states. Tapping an available feature navigates to its page; coming-soon cards remain informative and do not imply availability.

- [ ] **Step 5: Run the contract test and inspect the project in微信开发者工具**

Run: `node --test mini-program/services/fallback.test.js`
Expected: all fallback contract tests pass. Open `mini-program/` in微信开发者工具 and verify home page plus bottom tabs.

### Task 5: Documentation and end-to-end local verification

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Modify: `server/package.json`

- [ ] **Step 1: Document local startup**

Document `docker compose up -d mysql`, `npm install`, `npx prisma migrate dev`, `npm run seed`, `npm run dev`, API base URL configuration, and importing `mini-program/` into微信开发者工具.

- [ ] **Step 2: Start MySQL and initialize schema**

Run: `docker compose up -d mysql`; then `cd server && npx prisma migrate dev --name init && npm run seed`.
Expected: MySQL is healthy, migration succeeds, and seed inserts one platform config plus three feature entries.

- [ ] **Step 3: Run the full automated verification**

Run: `cd server && npm test -- --run && npm run typecheck && npm run build`
Expected: all tests pass, typecheck and build exit 0.

- [ ] **Step 4: Verify real HTTP responses**

Start the server and run `curl http://127.0.0.1:3000/api/health` and `curl http://127.0.0.1:3000/api/home/summary`.
Expected: health reports database `up`; summary contains all three feature entries from MySQL.

- [ ] **Step 5: Review final file diff**

Run: `git status --short` and inspect all changed files. Do not commit unless the repository becomes writable and the user explicitly wants commits.
