# Python DDD 服务端 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 `server/` 原地迁移为兼容现有前端 API 的 Python DDD 服务端。

**Architecture:** FastAPI 接收 HTTP 请求，application 层编排用例，domain 层定义模型和仓储端口，infrastructure 层使用 SQLAlchemy 访问现有 MySQL 表。Docker 和 Nginx 保持 3000 端口及 `/api/` 代理契约。

**Tech Stack:** Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.x, PyMySQL, Pydantic Settings, Alembic, pytest。

## Global Constraints

- 保留 `GET /api/health` 与 `GET /api/home/summary`。
- 兼容现有 `PlatformConfig`、`FeatureEntry` 表和 MySQL 数据。
- 不删除 MySQL volume，不在启动时重置数据。
- 前端无需修改 API 路径。

### Task 1: 建立 Python 项目骨架

**Files:**
- Delete: `server/src/`、`server/package.json`、`server/package-lock.json`、`server/tsconfig.json`、`server/vitest.config.ts`
- Create: `server/app/`、`server/tests/`、`server/pyproject.toml`、`server/.env.example`

- [ ] 创建 Python 包、依赖和 pytest 配置。
- [ ] 运行 `python -m compileall app tests`，确认骨架可编译。

### Task 2: 实现 domain/application 层

**Files:**
- Create: `server/app/domain/platform/models.py`
- Create: `server/app/domain/platform/repositories.py`
- Create: `server/app/application/home/get_home_summary.py`
- Test: `server/tests/unit/test_get_home_summary.py`

- [ ] 先写仓储 stub 测试，验证用例返回 `HomeSummary`。
- [ ] 定义不可变领域数据模型和仓储协议。
- [ ] 实现 `GetHomeSummary.execute()`。

### Task 3: 实现基础设施和 HTTP 接口

**Files:**
- Create: `server/app/infrastructure/config/settings.py`
- Create: `server/app/infrastructure/database/session.py`
- Create: `server/app/infrastructure/database/health.py`
- Create: `server/app/infrastructure/platform/sqlalchemy_repository.py`
- Create: `server/app/interfaces/http/app.py`
- Create: `server/app/interfaces/http/routes/health.py`
- Create: `server/app/interfaces/http/routes/home.py`
- Create: `server/app/main.py`
- Test: `server/tests/integration/test_http_api.py`

- [ ] 使用 SQLAlchemy 映射现有表名和列名。
- [ ] 用 FastAPI dependency 注入 Session 和用例。
- [ ] 实现 `/api/health` 与 `/api/home/summary`，并用 TestClient 验证响应结构。

### Task 4: 更新容器与部署文档

**Files:**
- Modify: `server/Dockerfile`
- Modify: `docker-compose.yml`
- Modify: `docker-compose.prod.yml`
- Modify: `README.md`

- [ ] 使用 Python 3.12 slim 镜像和 Uvicorn 启动。
- [ ] 保留 `DATABASE_URL`、`PORT` 和 MySQL 健康依赖。
- [ ] 更新本地启动、测试和部署说明。

### Task 5: 验证和提交

- [ ] 运行 `pytest -q`、`python -m compileall app tests`。
- [ ] 运行 Docker 构建和容器 API 验证。
- [ ] 检查 Git diff，提交 Python DDD 迁移。
