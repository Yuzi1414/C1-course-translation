# 构建一个远程 MCP 服务器 · Cloudflare Agents 文档

本指南将向你展示如何在 Cloudflare 上部署你自己的远程 MCP（模型上下文协议）服务器，使用 Streamable HTTP 传输——这是当前 MCP 规范的标准。你有两种选择：

- **无身份验证**——任何人都可以连接并使用该服务器（无需登录）。
- **带身份验证与授权**——用户先登录才能访问工具，并且你可以根据用户的权限控制智能体能够调用哪些工具。

## 选择一种方案

Agents SDK 提供了多种创建 MCP 服务器的方式。请选择适合你用例的方案：

| 方案 | 有状态？ | 需要 Durable Objects？ | 最适合 |
|---|---|---|---|
| `createMcpHandler()` | 否 | 否 | 无状态工具、最简单的设置 |
| `McpAgent` | 是 | 是 | 有状态工具、按会话的状态、elicitation（引导式交互） |
| 原生 `WebStandardStreamableHTTPServerTransport` | 否 | 否 | 完全控制、不依赖 SDK |

`createMcpHandler()` 是让无状态 MCP 服务器跑起来最快的方式。当你的工具不需要按会话保存状态时，用它即可。

`McpAgent` 为每个会话提供一个 Durable Object，内置状态管理、elicitation 支持，以及 SSE 与 Streamable HTTP 两种传输方式。

原生 transport 则让你拥有完全控制权——如果你想直接用 `@modelcontextprotocol/sdk` 而不借助 Agents SDK 的辅助工具。

## 部署你的第一个 MCP 服务器

你可以先部署一个无身份验证的公开 MCP 服务器 ↗，之后再添加用户身份验证与按范围（scoped）的授权。如果你已经知道自己的服务器需要身份验证，可以直接跳到下一节。

### 通过仪表盘

下面的按钮将引导你完成把示例 MCP 服务器 ↗ 部署到 Cloudflare 账号所需的全部步骤：

部署完成后，该服务器将在你的 `workers.dev` 子域名上线（例如 `remote-mcp-server-authless.your-account.workers.dev/mcp`）。你可以立即使用 AI Playground ↗（一个远程 MCP 客户端）、MCP inspector ↗ 或其他 MCP 客户端连接它。

系统会在你的 GitHub 或 GitLab 账号上为你的 MCP 服务器新建一个 git 仓库，并配置为每次你推送改动、或向仓库的 `main` 分支合并拉取请求时，自动部署到 Cloudflare。你可以克隆这个仓库，在本地开发，并开始用你自己的工具定制这个 MCP 服务器。

### 通过 CLI

你可以使用 Wrangler CLI 在本地机器上创建一个新的 MCP 服务器，并部署到 Cloudflare。

打开终端，运行以下命令：

```
npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

```
yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

```
pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

在设置过程中，选择以下选项：
- 对于“Do you want to add an AGENTS.md file to help AI coding tools understand Cloudflare APIs?（是否要添加 AGENTS.md 文件，帮助 AI 编码工具理解 Cloudflare API？）”，选择 **No**。
- 对于“Do you want to use git for version control?（是否要使用 git 做版本控制？）”，选择 **No**。
- 对于“Do you want to deploy your application?（是否要部署你的应用？）”，选择 **No**（我们会在部署之前先测试服务器）。

现在，你的 MCP 服务器已搭建完成，依赖也已安装。

进入项目文件夹：

```
cd remote-mcp-server-authless
```

在新项目的目录中，运行以下命令启动开发服务器：

```
npm start
```

```
┄ 正在启动本地服务器...

[wrangler:info] Ready on http://localhost:8788
```

检查命令输出里的本地端口。在这个例子中，MCP 服务器运行在 8788 端口，MCP 端点 URL 是 `http://localhost:8788/mcp`。

要在本地测试服务器：

在一个新终端中运行 MCP inspector ↗。MCP inspector 是一个交互式 MCP 客户端，让你从网页浏览器连接 MCP 服务器并调用工具。

```
npx @modelcontextprotocol/inspector@latest
```

```
🚀 MCP Inspector is up and running at:

http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3

🌐 Opening browser...
```

MCP Inspector 会在你的网页浏览器中启动。你也可以手动启动：打开浏览器并前往 `http://localhost:<PORT>`。检查命令输出里 MCP Inspector 运行的本地端口。在这个例子中，MCP Inspector 服务运行在 5173 端口。

在 MCP inspector 中，输入你 MCP 服务器的 URL（`http://localhost:8788/mcp`），然后选择 **Connect**。选择 **List Tools**，即可显示你的 MCP 服务器暴露出来的工具。

现在你可以把 MCP 服务器部署到 Cloudflare 了。在项目目录中运行：

```
npx wrangler@latest deploy
```

如果你已经把一个 git 仓库连接到了带 MCP 服务器的 Worker 上，你可以通过推送改动、或向仓库的 `main` 分支合并拉取请求来部署你的 MCP 服务器。

MCP 服务器将部署到你的 `*.workers.dev` 子域名，地址为 `https://remote-mcp-server-authless.your-account.workers.dev/mcp`。

要测试远程 MCP 服务器，把你已部署的 MCP 服务器 URL（`https://remote-mcp-server-authless.your-account.workers.dev/mcp`）输入到运行在 `http://localhost:5173` 的 MCP inspector 中。

现在你拥有了一个 MCP 客户端可以连接的远程 MCP 服务器。

## 通过本地代理从 MCP 客户端连接

现在你的远程 MCP 服务器已在运行，你可以使用 `mcp-remote` 本地代理 ↗ 把 Claude Desktop 或其他 MCP 客户端连接到它——即使你的 MCP 客户端在客户端这一侧不支持远程传输或授权也没关系。这让你可以用一个真实的 MCP 客户端来测试与远程 MCP 服务器交互的实际效果。

例如，要从 Claude Desktop 连接：

更新你的 Claude Desktop 配置，让它指向你 MCP 服务器的 URL：

```json
{
  "mcpServers": {
    "math": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://remote-mcp-server-authless.your-account.workers.dev/mcp"
      ]
    }
  }
}
```

重启 Claude Desktop 以加载 MCP 服务器。完成后，Claude 就能调用你的远程 MCP 服务器了。

要测试，可以让 Claude 使用你的某个工具。例如：

> Could you use the math tool to add 23 and 19?（你能用 math 工具计算 23 加 19 吗？）

Claude 应该会调用该工具，并展示由远程 MCP 服务器生成的结果。

要了解如何用其他 MCP 客户端使用远程 MCP 服务器，请参考 Test a Remote MCP Server（测试远程 MCP 服务器）。

## 添加身份验证

你之前部署的公开 MCP 服务器示例，允许任何客户端无需登录即可连接并调用工具。要为 MCP 服务器添加用户身份验证，你可以集成 Cloudflare Access 或第三方服务作为 OAuth 提供方。你的 MCP 服务器处理安全登录流程，并签发访问令牌，MCP 客户端可以使用这些令牌发起经过身份验证的工具调用。用户通过 OAuth 提供方登录，并使用按范围的权限，授权其 AI 智能体与你的 MCP 服务器暴露的工具进行交互。

### Cloudflare Access OAuth

你可以配置 MCP 服务器，要求用户通过 Cloudflare Access 进行身份验证。Cloudflare Access 充当身份聚合器，核验用户邮箱、来自你现有身份提供方（如 GitHub 或 Google）的信号，以及 IP 地址或设备证书等其他属性。当用户连接 MCP 服务器时，他们会被提示登录已配置的身份提供方，并且只有在通过你的 Access 策略时才会被授予访问权限。

有关分步部署指南，请参考 Secure MCP servers with Access for SaaS（用 Access 保护面向 SaaS 的 MCP 服务器）。

### 第三方 OAuth

你可以把 MCP 服务器连接到任何支持 OAuth 2.0 规范的 OAuth 提供方，包括 GitHub、Google、Slack、Stytch、Auth0、WorkOS 等。

下面的示例演示如何把 GitHub 用作 OAuth 提供方。

#### 步骤 1 —— 创建新的 MCP 服务器

运行以下命令，创建一个带 GitHub OAuth 的新 MCP 服务器：

```
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```
yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```
pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

现在，你的 MCP 服务器已搭建完成，依赖也已安装。进入该项目文件夹：

```
cd my-mcp-server-github-auth
```

你会注意到，在这个示例 MCP 服务器中，如果你打开 `src/index.ts`，主要区别在于 `defaultHandler` 被设置成了 `GitHubHandler`：

```typescript
import GitHubHandler from "./github-handler";

export default new OAuthProvider({
  apiRoute: "/mcp",
  apiHandler: MyMCP.serve("/mcp"),
  defaultHandler: GitHubHandler,
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/token",
  clientRegistrationEndpoint: "/register",
});
```

这确保你的用户会被重定向到 GitHub 进行身份验证。不过要让它跑通，你需要在下面的步骤中创建 OAuth 客户端应用。

#### 步骤 2 —— 创建 OAuth App

你需要创建两个 GitHub OAuth App ↗，才能把 GitHub 用作 MCP 服务器的身份验证提供方——一个用于本地开发，一个用于生产环境。

#### 步骤 2.1 —— 为本地开发创建新的 OAuth App

前往 `github.com/settings/developers` ↗，用以下设置创建一个新的 OAuth App：

- Application name（应用名称）：`My MCP Server (local)`
- Homepage URL（主页 URL）：`http://localhost:8788`
- Authorization callback URL（授权回调 URL）：`http://localhost:8788/callback`

对于刚创建的 OAuth App，把它的 client ID 添加为 `GITHUB_CLIENT_ID`，并生成一个 client secret，以 `GITHUB_CLIENT_SECRET` 添加到项目根目录的 `.env` 文件中——这个文件将用于本地开发中的密钥设置。

```
touch .env
echo 'GITHUB_CLIENT_ID="your-client-id"' >> .env
echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .env
cat .env
```

运行以下命令启动开发服务器：

```
npm start
```

你的 MCP 服务器现在运行在 `http://localhost:8788/mcp`。

在一个新终端中运行 MCP inspector ↗。MCP inspector 是一个交互式 MCP 客户端，让你从网页浏览器连接 MCP 服务器并调用工具。

```
npx @modelcontextprotocol/inspector@latest
```

在你的网页浏览器中打开 MCP inspector：

```
open http://localhost:5173
```

在 inspector 中，输入你 MCP 服务器的 URL：`http://localhost:8788/mcp`

在右侧主面板中，点击 **OAuth Settings** 按钮，然后点击 **Quick OAuth Flow**。

你应当会被重定向到 GitHub 的登录或授权页面。在授权 MCP 客户端（即 inspector）访问你的 GitHub 账号后，你会被重定向回 inspector。

点击侧边栏中的 **Connect**，你应该会看到 **List Tools** 按钮，它将列出你的 MCP 服务器暴露的工具。

#### 步骤 2.2 —— 为生产环境创建新的 OAuth App

你需要重复步骤 2.1，为生产环境创建一个新的 OAuth App。

前往 `github.com/settings/developers` ↗，用以下设置创建一个新的 OAuth App：

- Application name（应用名称）：`My MCP Server (production)`
- Homepage URL（主页 URL）：填写你已部署 MCP 服务器的 `workers.dev` URL（例如：`worker-name.account-name.workers.dev`）
- Authorization callback URL（授权回调 URL）：填写你已部署 MCP 服务器的 `workers.dev` URL 的 `/callback` 路径（例如：`worker-name.account-name.workers.dev/callback`）

对于刚创建的 OAuth App，使用 Wrangler CLI 添加 client ID 和 client secret：

```
npx wrangler secret put GITHUB_CLIENT_ID
```

```
npx wrangler secret put GITHUB_CLIENT_SECRET
```

```
npx wrangler secret put COOKIE_ENCRYPTION_KEY # 在这里添加任意随机字符串，例如 openssl rand -hex 32
```

设置 KV 命名空间：

a. 创建 KV 命名空间：

```
npx wrangler kv namespace create "OAUTH_KV"
```

b. 用生成的 KV ID 更新 `wrangler.jsonc` 文件：

```json
{
  "kvNamespaces": [
    {
      "binding": "OAUTH_KV",
      "id": "<YOUR_KV_NAMESPACE_ID>"
    }
  ]
}
```

把 MCP 服务器部署到你的 Cloudflare `workers.dev` 域名：

```
npm run deploy
```

使用 AI Playground ↗、MCP Inspector 或其他 MCP 客户端，连接运行在 `worker-name.account-name.workers.dev/mcp` 的服务器，并用 GitHub 进行身份验证。

## 后续步骤

- **MCP Tools（MCP 工具）**：向你的 MCP 服务器添加工具。
- **Authorization（授权）**：定制身份验证与授权。
