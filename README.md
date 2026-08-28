# A股投资策略平台

微信原生小程序 + Node.js/TypeScript DDD 后端 + Prisma/MySQL。

## 项目结构

```text
mini-program/  微信小程序前端
server/        Fastify 后端
  src/interfaces      HTTP 路由与响应映射
  src/application      用例编排
  src/domain           业务领域与仓储接口
  src/infrastructure   Prisma、MySQL、配置和健康检查
docker-compose.yml     本地 MySQL 8
```

## 本地启动

1. 启动数据库：`docker compose up -d mysql`
2. 初始化后端：

   ```bash
   cd server
   cp .env.example .env
   npm install
   npx prisma migrate dev --name init
   npm run seed
   npm run dev
   ```

3. 用微信开发者工具导入 `mini-program/`。
4. 若开发者工具不允许访问本机服务，在“详情 → 本地设置”勾选“不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书”。

开发环境 API 地址默认是 `http://127.0.0.1:3000`，可在 `mini-program/app.js` 和 `server/.env` 中调整。

## API

- `GET /api/health`：服务和 MySQL 健康检查。
- `GET /api/home/summary`：从 MySQL 读取欢迎页摘要和三个能力入口。

## 验证

```bash
cd server
npm test -- --run
npm run typecheck
npm run build
cd ..
node --test mini-program/services/fallback.test.js
```

首期不接入真实行情和交易数据；个股追踪、策略选股页面以“即将上线”状态展示，避免伪造金融数据。
