# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-05-28

### Added

- **FastAPI 后端**（`server/`）：完整的 Agent 服务端实现
  - LLM 接入层：OpenAI 兼容格式，支持 SSE 流式输出
  - 三层记忆系统：pgvector 向量检索 + CRUD API
  - 亲密度引擎：事件累加模型 + 连续活跃 bonus
  - Prompt Builder：将 6 章设计原则编译为动态 system prompt
- **数据库**：PostgreSQL + pgvector（docker-compose 一键启动）
- **前端改造**：对话/记忆/亲密度对接真实 API，移除硬编码回复
- 配置文件：`.env.example`、`requirements.txt`、`docker-compose.yml`、`init.sql`

### Changed

- 前端 `cases/huaxiaobei/index.html` 从静态 Demo 升级为可连接后端的完整应用
- README 新增技术架构图、API 文档、快速启动指南

[0.2.0]: https://github.com/keyuchen-del/Emotional-Companion-Agent/compare/v0.1.0...v0.2.0

## [0.1.0] - 2026-05-27

### Added

- **仓库通用化**：从 `Product-Design-for-Huabei` 重命名为 `Emotional-Companion-Agent`，定位为「情感陪伴 Agent 设计手册 + 案例集」
- **docs/ 设计手册**（6 章去品牌化设计原则）：
  - 01 三层记忆架构（先验/共建/默契）
  - 02 三序取舍原则（用户自主 > 系统建议 > 商业目标）
  - 03 坏消息五幕剧（通知 → 共情 → 解释 → 行动 → 闭环）
  - 04 三模态情绪表达（动作 + 表情 + 文字）
  - 05 关系成长体系
  - 06 禁区锚点 + 未完待续锚点
- **cases/huaxiaobei/** 首个完整实例（花小呗 · 支付宝花呗 AI 助手），含设计映射表、品牌特有设计决策、4 页可交互 Demo
- MIT LICENSE、CHANGELOG、.gitignore
- GitHub Pages redirect（根 index.html → cases/huaxiaobei/）

### Changed

- 根 README 从花呗专题改写为作品集门面

[0.1.0]: https://github.com/keyuchen-del/Emotional-Companion-Agent/releases/tag/v0.1.0
