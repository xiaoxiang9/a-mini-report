# A股投资策略平台

微信原生小程序 + React/Web + Python/FastAPI DDD 后端 + SQLAlchemy/MySQL。

## 项目结构

```text
mini-program/  微信小程序前端
server/        FastAPI Python 后端
  app/interfaces      HTTP 路由与响应映射
  app/application     用例编排
  app/domain          业务领域与仓储接口
  app/infrastructure  SQLAlchemy、MySQL、配置和健康检查
  migrations/         MySQL 兼容迁移基线
web/            React Web 前端
docker-compose.yml     本地 MySQL 8
```

## 本地启动

1. 启动数据库：`docker compose up -d mysql`
2. 初始化后端：

   ```bash
   cd server
   python3 -m venv .venv
   .venv/bin/pip install -e '.[dev]'
   cp .env.example .env
   .venv/bin/uvicorn app.main:app --reload --port 3000
   ```

3. 用微信开发者工具导入 `mini-program/`。
4. 若开发者工具不允许访问本机服务，在“详情 → 本地设置”勾选“不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书”。

开发环境 API 地址默认是 `http://124.220.34.112:3000`，可在 `mini-program/app.js` 和 `server/.env` 中调整。当前使用公网 IP 仅用于开发者工具验证；小程序生产发布需要备案域名和 HTTPS。任务管理页面还需要在 Web 环境配置 `VITE_TASK_ADMIN_TOKEN`，服务端配置 `TASK_ADMIN_TOKEN`。

## 腾讯云服务器部署

服务器执行一次初始化：

```bash
dnf install -y git docker-compose-plugin
systemctl enable --now docker
mkdir -p /opt/a-mini-report
```

GitHub Actions 会在 GitHub Runner 构建 Web，然后通过原生 `scp` 上传 `web/dist`、后端源码和 Nginx 配置，再在服务器执行 Docker Compose 更新。需要配置 `TENCENT_SERVER_HOST`、`TENCENT_SERVER_USER`、`TENCENT_SERVER_SSH_KEY`、`TENCENT_SERVER_PORT` 和服务器 `.env` 中的 `TUSHARE_TOKEN`。

Web 地址为 `https://myxiang.online/`，API 地址为 `https://myxiang.online/api/`。Nginx 配置模板位于 `deploy/nginx/myxiang.online.conf`。

## API

- `GET /api/health`：服务和 MySQL 健康检查。
- `GET /api/home/summary`：从 MySQL 读取欢迎页摘要和三个能力入口。
- `GET /api/stocks/tracking`：获取公共个股追踪列表。
- `GET /api/stocks/{ts_code}`：获取个股详情和估值历史。
- `POST /api/stocks/tracking`：添加股票，body 为 `{ "tsCode": "600519.SH" }`。
- `DELETE /api/stocks/{ts_code}`：取消追踪但保留历史数据。
- `POST /api/stocks/sync`：手动执行一次追踪股票同步。
- `GET /api/tasks`：查询全局定时任务（需 `X-Task-Admin-Token`）。
- `PATCH /api/tasks/{task_key}`：修改任务启停状态或每日执行时间。
- `POST /api/tasks/{task_key}/run`：立即执行任务并返回概况。
- `GET /api/tasks/{task_key}/logs`：查询任务执行记录。

个股数据优先使用 Tushare 的 `stock_basic`、`trade_cal`、`daily` 和 `daily_basic` 接口；PE/PB 历史百分位按上市日到最新交易日的有效历史估值计算，按时间片分段拉取并去重。生产 scheduler 默认每天 17:00（Asia/Shanghai）执行，也可在 Web 任务管理中修改。Token 仅通过环境变量 `TUSHARE_TOKEN` 配置。

数据库迁移按编号顺序执行：`server/migrations/0001_initial.sql`、`0002_stock_detail.sql`、`0003_task_center.sql`、`0004_stock_history_metadata.sql`。执行前请备份生产 MySQL；已有数据库升级时不要重复执行已完成的迁移。

## 验证

```bash
cd server
.venv/bin/python -m pytest -q
.venv/bin/python -m compileall app tests
docker build -t a-stock-platform-server .
cd ..
node --test mini-program/services/fallback.test.js
```

策略选股仍以“即将上线”状态展示；个股追踪数据只展示已从 Tushare 成功同步的真实数据，不使用伪造行情。
