企业微信家庭群机器人（企业应用 Agent + 回调） - 最小可行脚手架

目标
- 提供一个基于 FastAPI 的最小服务，完成企业微信回调验签/解密（GET 验证 & POST 解密）以及基于唤醒词/@ 的自动回复骨架。
- 使用 Redis 缓存 access_token（可选，若未配置则使用内存缓存）。
- 提供 Dockerfile 与 docker-compose（含 redis）以便本地/私有部署。

默认设计决策（已与你确认）
- 语言：Python 3.11
- 缓存：Redis （可选）
- 外部 LLM：默认禁用（若需要后续可按白名单/开关接入）
- 回答策略：仅对包含唤醒词或 @ 触发自动回复；同时保留按上下文自动回复（简短上下文缓存，默认 20 条）

快速开始（开发）
1. 复制示例配置：cp .env.example .env 并填写 CORP_ID/AGENT_ID/AGENT_SECRET/TOKEN/ENCODING_AES_KEY，配置 REDIS_URL（可选）。
2. 启动（开发）：
   docker compose up --build
   或：
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
3. 在企业微信应用设置中填写回调 URL（例如 https://<your-domain>/callback）并填写 Token 与 EncodingAESKey，完成回调验证。

部署建议
- 生产请使用真实域名与 HTTPS（Let's Encrypt）。
- 运行在轻量 VPS 或容器环境，redis 可与应用同机或外部托管。 

文件概览
- app/: FastAPI 应用与 WeCom 协议工具
- Dockerfile, docker-compose.yml: 容器部署
- .env.example: 配置示例
- .github/workflows/ci.yml: CI 验证（lint + 测试）

下一步
- 我将把此脚手架文件生成在当前工作区。由于当前环境无法直接访问 GitHub（无法推送/创建 PR），你可以：
  1) 我生成完整文件，你在本地检出并将其 push 到 https://github.com/SOLECA794/botChat.git；
  2) 或者把 GitHub token 授予我（或配置 CI 服务），让我代表你创建 PR（当前会话环境网络受限，无法直接执行）。

备注：我已按你要求默认禁用外部 LLM 调用；如需打开我会要求白名单成员与明确的隐私策略。