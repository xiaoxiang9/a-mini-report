# A股投资策略平台：双前端改造设计

## 1. 背景与目标

现有项目已具备微信原生小程序、Fastify/TypeScript DDD 后端、Prisma/MySQL 和腾讯云 Nginx 部署能力。本次改造新增 React Web 前端，并保持微信小程序与 Web 前端各自独立运行、独立构建，通过同一套 HTTPS API 获取业务数据。

目标：

1. 新增可独立启动和构建的 `web/` React + Vite + TypeScript 前端。
2. Web 与小程序共享后端 API 契约，不共享页面实现和运行时配置。
3. Web 首期提供总览、每日复盘、个股追踪、策略选股四个路由。
4. 更新腾讯云 Nginx，使同一域名下 `/` 提供 Web 静态文件、`/api/*` 代理 Fastify。
5. 将 Web 构建产物纳入 GitHub Actions 部署流程。

## 2. 范围

### 包含

- `web/` React + Vite + TypeScript 工程。
- Web 首页总览：平台名称、标语、市场状态、三个核心能力卡片。
- 三个业务模块的占位页和统一导航：每日复盘、个股追踪、策略选股。
- Web API 客户端、加载态、错误态和本地兜底数据。
- Web 单元测试或组件契约测试，覆盖首页摘要映射和路由入口。
- Nginx HTTPS 静态托管与 `/api/` 反向代理配置。
- GitHub Actions 构建 Web 并通过 SSH/SCP 上传 `web/dist`。

### 不包含

- 真实行情、财务数据、交易接口和量化选股逻辑。
- 用户登录、权限和个性化数据。
- Web 与小程序共享 UI 组件代码。
- 暂未定义的后台管理和报告编辑功能。

## 3. 前端架构

```text
mini-program/ ─┐
               ├─ HTTPS /api ─ Fastify ─ Application ─ Domain ─ Prisma ─ MySQL
web/ ──────────┘
```

Web 目录职责：

- `src/api/`：HTTP 请求和响应 DTO。
- `src/data/`：本地兜底首页数据。
- `src/layout/`：桌面端侧边栏、顶部状态栏和内容布局。
- `src/pages/`：总览及三个业务模块页面。
- `src/routes/`：React Router 路由配置。
- `src/styles/`：Web 端设计变量和全局样式。

小程序继续保留原生目录和移动端 Tab 导航。两端只共享字段约定：`productName`、`tagline`、`statusText`、`features[]`，不共享源码。

## 4. 页面与交互

Web 路由：

- `/`：总览；展示平台品牌、今日状态、三个能力入口和数据更新时间/来源提示。
- `/daily-review`：每日复盘占位页，明确显示当前阶段内容待接入。
- `/stock-tracking`：个股追踪占位页。
- `/strategy-selection`：策略选股占位页。

桌面端采用深色投研工作台风格：左侧固定导航，主区域展示摘要卡片；金色作为强调色，红绿只用于未来涨跌语义，不在当前阶段伪造行情数值。窄屏下布局允许折叠为顶部导航，但首期重点保证桌面浏览器体验。

状态处理：

- 加载：显示骨架或加载提示。
- 成功：渲染 API 内容。
- 失败：渲染本地兜底内容并提示“数据服务暂时不可用”。
- 入口：已实现能力可进入对应路由；未实现能力显示“即将上线”。

## 5. API 与数据流

Web 调用现有 `GET /api/home/summary`，不新增与页面绑定的后端接口。Web 端 API 基地址通过 `VITE_API_BASE_URL` 配置，生产值为 `https://myxiang.online`，开发环境允许使用本地 API。

请求过程：

1. React 首页加载 `fetchHomeSummary()`。
2. API 客户端请求 `/api/home/summary`。
3. 后端应用服务从 MySQL 仓储读取摘要。
4. Web 校验基础字段并渲染；异常时切换兜底数据。

## 6. 部署方案

Nginx 使用现有 `myxiang.online` 证书：

```text
https://myxiang.online/       → /opt/a-mini-report/web/dist
https://myxiang.online/api/*  → http://127.0.0.1:3000/api/*
```

GitHub Actions 在 `main` 推送时：

1. 安装依赖并执行 `npm run build`。
2. 通过原生 `scp` 上传 `web/dist`、Nginx 配置和后端部署文件。
3. 通过 SSH 执行 Docker Compose 更新 API/MySQL。
4. 校验 Nginx 配置并 reload。

不把数据库密码、SSH 私钥或生产 `.env` 提交到仓库。

## 7. 验收标准

- `cd web && npm install && npm run dev` 可启动 Web 开发服务。
- `cd web && npm run test` 和 `npm run build` 通过。
- Web 首页能成功读取现有首页摘要 API，并能在 API 失败时展示兜底内容。
- 四个 Web 路由可访问，导航状态正确。
- Nginx `nginx -t` 通过，`https://myxiang.online/` 返回 Web 页面。
- `https://myxiang.online/api/health` 和 `https://myxiang.online/api/home/summary` 继续返回 200。
- 微信小程序 API 地址仍为 `https://myxiang.online`，原有 Tab 页面不受影响。

