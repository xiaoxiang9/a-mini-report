# Python DDD 服务端设计

## 目标

将当前 `server/` 从 Node.js/Fastify/Prisma 迁移为 Python 服务端，采用 DDD 分层与按领域组织代码，保留微信小程序和 Web 前端当前使用的 HTTP API。

## 边界

- 本阶段实现 `GET /api/health` 与 `GET /api/home/summary`。
- MySQL 继续使用现有 `PlatformConfig`、`FeatureEntry` 表及数据，不执行破坏性重建。
- 每日复盘、个股追踪、策略选股只保留领域扩展边界，不在本阶段虚构业务数据。
- 前端不改 API 路径；Nginx 继续代理 `/api/` 到容器 3000 端口。

## 架构

`interfaces/http` 负责 FastAPI 路由、请求生命周期和响应模型；`application` 负责用例编排；`domain` 只定义领域实体、仓储端口和业务错误；`infrastructure` 提供 SQLAlchemy MySQL 实现、配置和数据库健康检查。依赖方向由外向内，领域层不依赖 FastAPI 或 SQLAlchemy。

```text
HTTP -> interfaces -> application -> domain <- infrastructure
                         |
                         +-- MySQL repository implementation
```

## 技术选择

- Python 3.12
- FastAPI + Uvicorn
- SQLAlchemy 2.x + PyMySQL
- Pydantic Settings
- pytest
- Alembic 作为后续迁移入口，本阶段以现有数据库结构为兼容基线

## 数据流

首页请求经过路由进入 `GetHomeSummary` 用例，由 `HomeSummaryRepository` 端口读取平台配置和按 `sort_order` 排序的功能入口，映射为稳定 JSON。数据库不可用时健康检查返回 `down`；未找到首页配置或未处理异常返回统一错误响应，不把基础设施对象泄露给前端。

## 验收标准

- `pytest` 覆盖领域映射、健康检查和首页 API。
- `python -m compileall app tests` 通过。
- Docker 镜像可构建并启动，容器内 API 可访问。
- `/api/home/summary` 返回字段与现有前端类型一致。
- 不删除现有 MySQL volume、环境变量或 Nginx HTTPS 配置。
