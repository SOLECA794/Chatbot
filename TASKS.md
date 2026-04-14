WeCom 家庭群 Agent — 任务清单（按优先级）

说明：该清单保存在仓库目录 botChat-scaffold/ 中，作为外部、可跟踪的执行清单。负责人默认 Hermes Agent（我），你作为项目管理员/审核者。每项完成后我会更新状态并在 PR/Issue 中记录进度。

1) 仓库与凭证（已完成）
   - 状态：已完成（本地）
   - 说明：.env 已按你提供内容写入 botChat-scaffold/.env（仅本地文件）。

2) 推送 scaffold 到 GitHub 仓库
   - 负责人：你（由你 push）
   - 状态：待办
   - 输出：feat/scaffold 分支 + PR
   - 估时：0.1d

3) 回调基础（GET 验证 & POST 解密）
   - 负责人：Hermes Agent
   - 状态：待办
   - 任务：实现 WXBizMsgCrypt 验签/解密、GET echostr 验证返回、POST 解密并解析消息日志
   - PR：feat/wecom-callback
   - 估时：0.5d

4) access_token 缓存与发送能力
   - 负责人：Hermes Agent
   - 状态：待办
   - 任务：实现 Redis 缓存（或内存回退）、access_token 自动刷新、基础 message/send 文本回复
   - PR：feat/token-send
   - 估时：0.5d

5) 群消息识别与回复策略
   - 负责人：Hermes Agent
   - 状态：待办
   - 任务：识别群消息、@ 识别、唤醒词、白名单/黑名单控制、冷却与防循环
   - PR：feat/group-handling
   - 估时：0.5d

6) 媒体处理（图片/语音）基础
   - 负责人：Hermes Agent
   - 状态：待办
   - 任务：实现 media upload/download 流程、消息中图片的解析（存临时）、并可回复图片
   - PR：feat/media
   - 估时：1d

7) 集成测试与安全审查
   - 负责人：Hermes Agent + 你（验收）
   - 任务：端到端回调测试（ngrok 或真域名）、安全检查（不在日志记录 secret、验证回调来源）、隐私策略验证（上下文清除）
   - 状态：待办
   - 估时：0.5d

8) 部署与运行文档
   - 负责人：Hermes Agent
   - 任务：撰写生产部署说明（域名/证书/Nginx/监控）、GitHub Actions Secrets 指南
   - 状态：待办
   - 估时：0.5d

9) 可选：管理面板（白名单/日志清理）
   - 负责人：后续决定
   - 状态：待办
   - 估时：1-2d

备注：若你在任一阶段希望我直接在仓库中提交改动（而非你 push），请提前提供短期 PAT（仅在需要时请求），我会在 PR 中注明并把凭证使用记录清楚。