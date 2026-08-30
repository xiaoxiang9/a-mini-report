# 个股追踪模块 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现个人平台级个股追踪列表、详情、添加/移除、Tushare 数据同步及每日 17:00 定时任务。

**Architecture:** Domain 层定义股票详情、仓储和数据提供者协议；Application 层编排追踪操作和同步；Infrastructure 层用 SQLAlchemy、MySQL、Tushare 实现适配；HTTP 层向 Web 与微信小程序提供稳定 JSON。scheduler 作为独立进程运行，避免 API 多实例重复同步。

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.x, PyMySQL, Pydantic Settings, Tushare, APScheduler, pytest, React, 微信原生小程序。

## Global Constraints

- 第一阶段是平台级公共列表，不区分用户。
- 内部代码统一使用 `600519.SH`、`000001.SZ` 格式。
- 最近 7 天指最近 7 个交易日；PE/PB 百分位只使用有效正数历史值。
- Tushare Token 只从 `TUSHARE_TOKEN` 环境变量读取，不写入代码、数据库或前端。
- 同步失败保留上次有效数据并记录错误；不伪造金融数据。
- 删除只取消追踪，不删除股票历史数据。
- 每天 17:00 使用 `Asia/Shanghai` 时区执行。

### Task 1: 领域模型与计算服务

**Files:**
- Create: `server/app/domain/stock_tracking/models.py`
- Create: `server/app/domain/stock_tracking/repositories.py`
- Create: `server/app/domain/stock_tracking/providers.py`
- Create: `server/app/application/stock_tracking/calculations.py`
- Test: `server/tests/unit/stock_tracking/test_calculations.py`

- [ ] 先测试代码标准化、7 日涨幅和历史百分位。
- [ ] 实现纯函数，输入缺失数据返回 `None` 而不是 0。
- [ ] 定义仓储和 Tushare provider Protocol，不让领域依赖第三方库。
- [ ] 运行 `.venv/bin/python -m pytest -q server/tests/unit/stock_tracking/test_calculations.py`。

### Task 2: MySQL 表和仓储

**Files:**
- Create: `server/migrations/0002_stock_detail.sql`
- Create: `server/app/infrastructure/stock_tracking/sqlalchemy_repository.py`
- Test: `server/tests/unit/stock_tracking/test_repository.py`

- [ ] 建立 `StockDetail` 表和 `ts_code` 唯一索引。
- [ ] 实现追踪列表、详情、upsert、取消追踪和同步错误更新。
- [ ] 用 SQLite 测试 SQLAlchemy repository 的字段映射和排序。

### Task 3: Tushare provider 与同步用例

**Files:**
- Modify: `server/pyproject.toml`
- Modify: `server/app/infrastructure/config/settings.py`
- Create: `server/app/infrastructure/stock_tracking/tushare_provider.py`
- Create: `server/app/application/stock_tracking/list_tracked_stocks.py`
- Create: `server/app/application/stock_tracking/get_stock_detail.py`
- Create: `server/app/application/stock_tracking/add_tracked_stock.py`
- Create: `server/app/application/stock_tracking/remove_tracked_stock.py`
- Create: `server/app/application/stock_tracking/sync_tracked_stocks.py`
- Test: `server/tests/unit/stock_tracking/test_sync.py`

- [ ] Tushare provider 调用 `stock_basic`、`trade_cal`、`daily`、`daily_basic`。
- [ ] 对每只股票独立捕获 provider 错误，成功结果和失败结果分别返回。
- [ ] 实现添加时校验股票存在，删除只更新 `is_tracked=false`。
- [ ] 用 fake provider 测试同步成功、空数据和单只失败隔离。

### Task 4: HTTP API

**Files:**
- Create: `server/app/interfaces/http/routes/stocks.py`
- Modify: `server/app/interfaces/http/app.py`
- Test: `server/tests/integration/test_stock_tracking_api.py`

- [ ] 实现 `GET /api/stocks/tracking`、`GET /api/stocks/{ts_code}`、`POST /api/stocks/tracking`、`DELETE /api/stocks/{ts_code}`、`POST /api/stocks/sync`。
- [ ] 响应字段使用前端约定的 camelCase。
- [ ] 测试 200、404、409、422 和同步结果响应。

### Task 5: 17:00 scheduler 与容器

**Files:**
- Create: `server/app/scheduler/stock_sync.py`
- Modify: `server/Dockerfile`
- Modify: `docker-compose.prod.yml`
- Modify: `server/.env.example`
- Test: `server/tests/unit/stock_tracking/test_scheduler.py`

- [ ] 用 APScheduler CronTrigger 设置 `hour=17, minute=0, timezone=Asia/Shanghai`。
- [ ] 增加独立 `scheduler` Compose 服务，共享 API 镜像和环境变量。
- [ ] Token 缺失时任务记录可诊断错误并退出当前轮次。

### Task 6: 双前端列表和详情

**Files:**
- Modify: `web/src/api/stocks.ts`
- Modify: `web/src/pages/ModulePage.tsx`
- Modify: `web/src/App.tsx`
- Modify: `mini-program/pages/stock-tracking/*`
- Test: `web/src/api/stocks.test.ts`

- [ ] Web 和小程序展示列表指标、空状态、加载状态和数据日期。
- [ ] 点击列表项进入详情，添加和移除操作调用 API 并刷新列表。
- [ ] 生产数据缺失时显示“暂无数据”，不展示虚假数值。

### Task 7: 全量验证与提交

- [ ] 运行服务端 pytest、compileall、Web 测试和构建。
- [ ] 使用本机 MySQL 执行迁移，启动 API 后验证真实列表和详情接口。
- [ ] 使用 fake provider 验证同步流程，不在没有 Token 时请求 Tushare。
- [ ] 检查 `git diff --check`、忽略缓存文件并提交推送。
