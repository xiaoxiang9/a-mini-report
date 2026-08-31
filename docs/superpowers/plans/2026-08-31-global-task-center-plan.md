# 全局任务中心与上市以来估值 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将估值百分位改为上市以来，并实现独立的全局任务管理、执行日志、调度控制和 Web 管理端。

**Architecture:** 股票同步继续作为任务处理器，通用任务中心只负责配置、调度、运行状态和日志。任务配置与执行日志持久化到 MySQL，API 负责管理操作，独立 scheduler 负责从数据库装载启用任务并运行。

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy, MySQL, APScheduler, Tushare, pytest, React/Vite。

## Global Constraints

- 任务中心是平台级能力，不归属股票或其他业务模块。
- 当前注册 `stock-detail-daily-sync`，默认 17:00 Asia/Shanghai。
- 管理接口使用 `X-Task-Admin-Token` 与 `TASK_ADMIN_TOKEN` 校验。
- 百分位起点使用 `stock_basic.list_date`，历史数据必须分段、去重和排序。
- 不删除现有股票、平台配置和历史数据。

### Task 1: 上市以来估值百分位

**Files:**
- Modify: `server/app/domain/stock_tracking/providers.py`
- Modify: `server/app/infrastructure/stock_tracking/tushare_provider.py`
- Modify: `server/app/application/stock_tracking/calculations.py`
- Test: `server/tests/unit/stock_tracking/test_tushare_provider.py`

- [x] 测试 `stock_basic.list_date` 被作为起始日期。
- [x] 分段请求 `daily_basic`，合并并按交易日去重。
- [x] 保存历史起止日期和样本数量到快照元数据。
- [x] 运行 provider 与全量服务端测试。

### Task 2: 全局任务领域和数据库

**Files:**
- Create: `server/app/domain/task/models.py`
- Create: `server/app/domain/task/repositories.py`
- Create: `server/app/application/task/services.py`
- Create: `server/app/infrastructure/task/sqlalchemy_repository.py`
- Create: `server/migrations/0003_task_center.sql`
- Tests: `server/tests/unit/task/test_services.py`, `server/tests/unit/task/test_repository.py`

- [x] 定义任务配置、执行日志和状态枚举。
- [x] 实现任务列表、启停、时间校验、执行记录查询和日志写入。
- [x] 使用 SQLAlchemy 仓储持久化配置和日志。
- [x] 迁移使用 `CREATE TABLE IF NOT EXISTS`，可重复执行。

### Task 3: 通用 scheduler runtime

**Files:**
- Create: `server/app/scheduler/registry.py`
- Modify: `server/app/scheduler/stock_sync.py`
- Create: `server/app/scheduler/runtime.py`
- Test: `server/tests/unit/task/test_runtime.py`

- [x] 用 handler registry 注册股票同步处理器。
- [x] scheduler 从数据库加载 enabled 任务，按任务时区创建 CronTrigger。
- [x] 修改配置后刷新 job，禁止同一任务并发运行。
- [x] 每次执行写入 success/failed、耗时、成功数、失败数和概述。

### Task 4: 任务管理 API 和 Token 保护

**Files:**
- Create: `server/app/interfaces/http/routes/tasks.py`
- Modify: `server/app/interfaces/http/app.py`
- Modify: `server/app/infrastructure/config/settings.py`
- Test: `server/tests/integration/test_task_api.py`

- [x] 实现 `/api/tasks`、`PATCH /api/tasks/{task_key}`、`POST /api/tasks/{task_key}/run`、`GET /api/tasks/{task_key}/logs`。
- [x] 缺少或错误 Token 返回 401，Token 不写入响应。
- [x] 修改时间仅允许 00:00-23:59，启停和日志响应可追踪。

### Task 5: Web 任务管理页面

**Files:**
- Create: `web/src/api/tasks.ts`
- Create: `web/src/pages/TaskManagementPage.tsx`
- Modify: `web/src/App.tsx`
- Modify: `web/src/layout/AppLayout.tsx`
- Modify: `web/src/styles/global.css`
- Test: `web/src/api/tasks.test.ts`

- [x] 展示任务状态、启用状态、执行时间、上下次运行时间和概述。
- [x] 支持启停、修改小时分钟、手动运行和查看日志。
- [x] 从 `VITE_TASK_ADMIN_TOKEN` 读取 Token，不在源码硬编码。

### Task 6: 容器配置、文档与验证

**Files:**
- Modify: `server/.env.example`
- Modify: `.env.production.example`
- Modify: `docker-compose.prod.yml`
- Modify: `README.md`

- [x] 增加 `TASK_ADMIN_TOKEN` 和 scheduler 环境配置。
- [x] 运行服务端 pytest、compileall、Web 测试和构建。
- [ ] 执行本机 MySQL 迁移，验证任务 API 和日志（本机 MySQL 未启动）。
- [ ] 检查 diff、提交并推送 GitHub。
