# 股票标签体系 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为个股追踪增加可维护的二层标签体系、标签筛选和股票打标能力。

**Architecture:** 标签作为独立 DDD 子域保存标签类型、标签内容和股票关联关系；股票列表通过查询组装标签信息。Web 端使用 Ant Design Modal、Form、Select、Tag 和 Table，标签配置与股票打标分别使用独立弹框。

**Tech Stack:** FastAPI、SQLAlchemy text SQL、MySQL、React、TypeScript、Ant Design、Vitest。

## Global Constraints

- 一级标签只表示标签类型，不直接用于股票打标。
- 二级标签归属一个一级标签，用于股票打标。
- 已被管理股票使用的二级标签禁止删除；后端必须强制校验。
- 股票名称和股票代码仍是固定列，不进入表头配置；标签列为普通可配置列。
- 股票追踪列表和标签筛选均通过 HTTP API，前端不直连 MySQL。

### Task 1: 标签领域模型与数据库迁移

**Files:**
- Create: `server/app/domain/tags/models.py`
- Create: `server/app/domain/tags/repositories.py`
- Create: `server/app/infrastructure/tags/sqlalchemy_repository.py`
- Create: `server/migrations/0006_stock_tags.sql`
- Test: `server/tests/unit/tags/test_models.py`

- [ ] **Step 1: Write failing tests** for category/tag naming validation, duplicate tag rejection, and assignment delete protection.
- [ ] **Step 2: Run `server/.venv/bin/pytest server/tests/unit/tags/test_models.py -q` and confirm failure because the tag domain does not exist.**
- [ ] **Step 3: Implement immutable category/tag/assignment models and repository interfaces.**
- [ ] **Step 4: Add MySQL tables `stock_tag_categories`, `stock_tags`, and `stock_tag_assignments` with unique names, foreign keys, and indexes.**
- [ ] **Step 5: Run the focused test and confirm it passes.**

### Task 2: 标签应用服务与 HTTP API

**Files:**
- Create: `server/app/application/tags/service.py`
- Create: `server/app/interfaces/http/routes/tags.py`
- Modify: `server/app/interfaces/http/app.py`
- Test: `server/tests/integration/test_tags_api.py`

- [ ] **Step 1: Write failing API tests** for listing nested tags, category/tag CRUD, rejecting deletion of used tags, and replacing stock assignments.
- [ ] **Step 2: Run the focused integration tests and confirm the expected 404/500 failures before implementation.**
- [ ] **Step 3: Implement endpoints: `GET /api/tags`, category POST/PATCH/DELETE, tag POST/PATCH/DELETE, `GET /api/stocks/{ts_code}/tags`, and `PUT /api/stocks/{ts_code}/tags`.**
- [ ] **Step 4: Return precise domain error codes such as `TAG_CATEGORY_NOT_EMPTY`, `TAG_IN_USE`, `TAG_NAME_DUPLICATE`, and map them to HTTP 409/422.**
- [ ] **Step 5: Run the focused integration tests and then the existing server test suite.**

### Task 3: 股票列表标签数据与筛选查询

**Files:**
- Modify: `server/app/domain/stock_tracking/models.py`
- Modify: `server/app/infrastructure/stock_tracking/sqlalchemy_repository.py`
- Modify: `server/app/interfaces/http/routes/stocks.py`
- Modify: `web/src/api/stocks.ts`
- Test: `server/tests/integration/test_stock_tracking_api.py`
- Test: `web/src/pages/stockTagging.test.ts`

- [ ] **Step 1: Write failing tests** asserting tracking responses expose `tags` and the frontend filter helper keeps stocks matching selected tag IDs by category.
- [ ] **Step 2: Run both focused tests and confirm failure because stock responses have no tags.**
- [ ] **Step 3: Extend `StockDetail`/`StockResponse` with `tags: StockTag[]`, load tags with a left join/secondary query, and preserve empty arrays for untagged stocks.**
- [ ] **Step 4: Add typed Web API methods and a pure `filterStocksByTags` helper.**
- [ ] **Step 5: Run focused tests and the existing frontend tests.**

### Task 4: Web 标签配置、筛选和股票打标

**Files:**
- Modify: `web/src/api/stocks.ts`
- Modify: `web/src/pages/StockTrackingPage.tsx`
- Modify: `web/src/pages/StockTrackingPage.test.tsx`
- Modify: `web/src/styles/global.css`

- [ ] **Step 1: Write failing component tests** for the 标签配置 button, category/tag management controls, tag filters, tag column, and stock tag modal save action.
- [ ] **Step 2: Run the focused component tests and confirm the controls are absent.**
- [ ] **Step 3: Add `标签配置` beside `表头配置`; implement nested CRUD UI, disable delete for tags with `usageCount > 0`, and refresh data after changes.**
- [ ] **Step 4: Render one `Select` per category below the collapsed search row; apply selections together with existing filters.**
- [ ] **Step 5: Add a `标签` table column with Ant `Tag` chips; clicking a row’s tag cell opens multi-select assignment modal and saves through PUT.**
- [ ] **Step 6: Run Web tests and production build; fix layout/scroll width regressions.**

### Task 5: Migration and local acceptance

**Files:**
- Modify: `.github/workflows/deploy.yml`
- Modify: `README.md` if setup instructions need the new migration.

- [ ] **Step 1: Add migration `0006_stock_tags.sql` to the deployment migration list.**
- [ ] **Step 2: Apply the migration locally against MySQL and verify all three tables and foreign keys.**
- [ ] **Step 3: Start the API and Web dev server, smoke test tag CRUD, stock assignment, filtering, and deletion protection.**
- [ ] **Step 4: Run the complete backend and frontend test/build commands and record results.**
- [ ] **Step 5: Review `git diff` for secrets, unrelated changes, and API compatibility.**
