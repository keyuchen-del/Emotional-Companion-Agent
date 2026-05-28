<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/growing-heart_1f497.png" width="64" height="64" alt="Emotional Companion Agent" />
</p>

<h1 align="center">Emotional Companion Agent</h1>

<p align="center">
  <strong>情感陪伴 AI Agent 设计手册 + 可运行系统</strong><br/>
  <sub>从「工具」到「伙伴」—— 让用户合上手机时心里蹦出一句「TA 懂我」</sub>
</p>

<p align="center">
  <a href="https://keyuchen-del.github.io/Emotional-Companion-Agent/">在线 Demo</a> &nbsp;|&nbsp;
  <a href="#设计亮点">设计亮点</a> &nbsp;|&nbsp;
  <a href="#技术架构">技术架构</a> &nbsp;|&nbsp;
  <a href="#快速启动">快速启动</a> &nbsp;|&nbsp;
  <a href="#路线图">路线图</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/pgvector-Vector_Search-336791?logo=postgresql&logoColor=white" alt="pgvector" />
  <img src="https://img.shields.io/badge/OpenAI-SSE_Streaming-412991?logo=openai&logoColor=white" alt="OpenAI" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" alt="Docker" />
  <img src="https://github.com/keyuchen-del/Emotional-Companion-Agent/actions/workflows/deploy-pages.yml/badge.svg" alt="Deploy" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
</p>

---

## 这是什么

一个面向**情感陪伴型 AI Agent** 的完整项目，包含两个层次：

- **设计手册** [`docs/`](docs/)：6 章去品牌化设计原则，适用于任何需要与用户建立长期情感关系的 Agent
- **可运行系统** [`server/`](server/)：FastAPI 后端 + pgvector 向量记忆 + OpenAI 流式对话，完整实现设计手册中的三层记忆、亲密度引擎和坏消息五幕剧

> **在线体验：**[Live Demo](https://keyuchen-del.github.io/Emotional-Companion-Agent/) 提供 4 个可交互页面（智能对话 / 亲密度 / 记忆小本本 / 拒额五幕剧），无需配置即可体验。启动后端后可对接真实 LLM。

## 设计亮点

| 章节 | 设计原则 | 核心理念 |
|------|----------|----------|
| [01](docs/01-three-layer-memory.md) | **三层记忆架构** | 先验层（系统已知）· 共建层（用户告知）· 默契层（互动沉淀），解决「开箱即懂你」与「不被监控」的张力 |
| [02](docs/02-three-order-principle.md) | **三序取舍原则** | 用户自主 > 系统建议 > 商业目标，任何违反此顺序的发言视为设计失败 |
| [03](docs/03-bad-news-five-acts.md) | **坏消息五幕剧** | 通知 → 共情 → 解释 → 行动 → 闭环，72 小时后主动回访是最关键的一笔 |
| [04](docs/04-tri-modal-emotion.md) | **三模态情绪表达** | 动作 + 表情 + 文字，纯文字 AI 无法复制的护城河 |
| [05](docs/05-relationship-growth.md) | **关系成长体系** | 亲密度赛季 + 连续活跃 bonus + 等级特权，让用户愿意持续投入关系 |
| [06](docs/06-memory-anchors.md) | **禁区锚点 + 未完待续锚点** | 记忆中最微妙的两个维度 — 用户明示「不要碰」的区域和上次对话留下的开放钩子 |

### Demo 页面

```
在线 Demo（手机模拟器）
├── 智能对话    ← AI 流式聊天 + 快捷回复 + 情绪感知
├── 亲密度      ← 赛季机制 + 等级特权 + 成长曲线
├── 小本本      ← 三层记忆可视化（先验/共建/默契）+ 禁区锚点
└── 拒额五幕剧  ← 坏消息场景完整交互演示（5 幕推进）
```

## 技术架构

```
┌────────────────────────────────────────────────────┐
│  Frontend (SSE Streaming)                          │
│  cases/huaxiaobei/index.html  ← 4 页可交互 Demo   │
└──────────────────────┬─────────────────────────────┘
                       │ HTTP / SSE
┌──────────────────────▼─────────────────────────────┐
│  FastAPI Backend  (server/)                         │
│  ┌──────────┐  ┌───────────┐  ┌─────────────────┐  │
│  │ Chat     │  │ Memory    │  │ Intimacy        │  │
│  │ Router   │  │ Router    │  │ Router          │  │
│  └────┬─────┘  └─────┬─────┘  └────────┬────────┘  │
│       │               │                 │           │
│  ┌────▼───────────────▼─────────────────▼────────┐  │
│  │  Services Layer                               │  │
│  │  • LLM (OpenAI-compatible, streaming)         │  │
│  │  • Prompt Builder (6 章原则 → system prompt)  │  │
│  │  • Memory (三层记忆 + pgvector 向量检索)      │  │
│  │  • Intimacy (事件累加 + 连续天数 bonus)       │  │
│  └───────────────────────┬───────────────────────┘  │
└──────────────────────────┼──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│  PostgreSQL + pgvector                              │
│  memories │ conversations │ intimacy_events          │
└─────────────────────────────────────────────────────┘
```

### 项目结构

```
Emotional-Companion-Agent/
├── docs/                        # 设计手册（6 章）
│   ├── 01-three-layer-memory    # 三层记忆架构
│   ├── 02-three-order-principle # 三序取舍原则
│   ├── 03-bad-news-five-acts    # 坏消息五幕剧
│   ├── 04-tri-modal-emotion     # 三模态情绪表达
│   ├── 05-relationship-growth   # 关系成长体系
│   └── 06-memory-anchors        # 禁区锚点 + 未完待续锚点
│
├── server/                      # FastAPI 后端（~800 行）
│   ├── main.py                  # 应用入口 + CORS + 静态文件挂载
│   ├── config.py                # 环境变量配置
│   ├── database.py              # 异步数据库连接
│   ├── auth.py                  # Bearer Token 认证
│   ├── models/
│   │   ├── db_models.py         # SQLAlchemy 表定义
│   │   └── schemas.py           # Pydantic 请求/响应模型
│   ├── routers/
│   │   ├── chat.py              # /api/chat — 流式对话
│   │   ├── memory.py            # /api/memories — 三层记忆 CRUD
│   │   └── intimacy.py          # /api/intimacy — 亲密度查询
│   └── services/
│       ├── llm.py               # OpenAI 兼容 LLM 调用
│       ├── prompt_builder.py    # 6 章原则 → 动态 system prompt
│       ├── memory_service.py    # 向量检索 + 记忆管理
│       └── intimacy_service.py  # 事件累加 + bonus 计算
│
├── cases/huaxiaobei/            # 首个落地案例（花小呗）
│   └── index.html               # 4 页可交互 Demo（808 行）
│
├── docker-compose.yml           # PostgreSQL + pgvector 一键启动
├── init.sql                     # 数据库初始化脚本
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量模板
├── index.html                   # 展示落地页（手机模拟器框架）
├── landing.css                  # 落地页样式
├── CHANGELOG.md                 # 版本变更记录
└── LICENSE                      # MIT
```

### API 接口

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | `/api/chat` | 流式对话（SSE），自动提取记忆 + 更新亲密度 |
| GET | `/api/memories/{user_id}` | 查询三层记忆（按层分类） |
| POST | `/api/memories` | 新增共建层记忆 |
| PUT | `/api/memories/{id}` | 编辑记忆内容 |
| DELETE | `/api/memories/{id}` | 删除记忆 |
| GET | `/api/intimacy/{user_id}` | 获取亲密度分数 + 等级 |

## 快速启动

### 方式一：仅体验前端 Demo

```bash
# 直接打开
open index.html

# 或启动本地服务器
python3 -m http.server 4173
# 访问 http://127.0.0.1:4173/
```

### 方式二：完整后端 + LLM 对话

```bash
# 1. 克隆项目
git clone https://github.com/keyuchen-del/Emotional-Companion-Agent.git
cd Emotional-Companion-Agent

# 2. 启动数据库
docker-compose up -d

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 LLM API Key 和 Base URL

# 5. 启动服务
uvicorn server.main:app --reload --port 8000

# 6. 访问 http://localhost:8000
```

支持任何 OpenAI 兼容格式的 LLM API（GPT-4o / Claude / 通义千问 / DeepSeek 等），只需修改 `.env` 中的 `LLM_BASE_URL` 和 `LLM_MODEL`。

## 已落地案例

### [花小呗 · 支付宝花呗 AI 助手](cases/huaxiaobei/)

首个完整实例。以花呗 AI 助手「花小呗」为载体，完整落地 6 章设计原则：

- **静态预览**：[GitHub Pages Demo](https://keyuchen-del.github.io/Emotional-Companion-Agent/)（手机模拟器框架）
- **完整体验**：启动后端后对话由真实 LLM 驱动

## 路线图

- [x] 通用化设计手册（6 章去品牌化原则）
- [x] 首个落地案例（花小呗 · 4 页可交互 Demo）
- [x] MVP 后端（FastAPI + pgvector + 三层记忆 + 亲密度）
- [x] 展示落地页（手机模拟器 + 产品介绍）
- [ ] 多角色支持（不同 Agent 人设 + 话术风格）
- [ ] 情绪识别增强（基于对话上下文的多维度情绪分析）
- [ ] 语音交互（TTS + ASR 接入）
- [ ] 记忆衰减机制（时间加权的记忆重要度排序）
- [ ] 多用户管理 + 登录注册
- [ ] 对话历史导出与分析
- [ ] 移动端 PWA 支持
- [ ] 更多落地案例（教育辅导 / 心理陪伴 / 老年关怀）

## 版本

当前版本 **v0.2.0** — MVP 后端 + 真实 API 对接

查看 [CHANGELOG](CHANGELOG.md) | [Releases](https://github.com/keyuchen-del/Emotional-Companion-Agent/releases)

## License

[MIT](LICENSE)

## 作者

**Jacky（陈柯宇）** · 北京大学汇丰商学院 金融硕士在读

---

*方案围绕一个用户可感知的终点展开：合上手机时，心里蹦出一句「TA 懂我」。*
