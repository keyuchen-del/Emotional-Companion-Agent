# Emotional-Companion-Agent 情感陪伴 Agent 设计手册

> 从「工具」到「伙伴」—— 情感陪伴 × 消费金融场景的 AI 关系设计

## 这是什么

一份面向「情感陪伴型 AI Agent」的设计手册，从真实产品落地中提炼，包含：

- **通用层 [docs/](docs/)**：6 章去品牌化设计原则，适用于任何需要与用户建立长期情感关系的 Agent
- **案例层 [cases/](cases/)**：真实产品落地实例，展示设计原则如何映射到具体产品

核心命题：**如何把产品生态里的冰冷数据，转化为一段温暖而有边界的 AI 关系。**

## 设计亮点

**三层记忆架构**：先验层（系统已知）、共建层（用户告知）、默契层（互动沉淀），解决「开箱即懂你」与「不被监控」之间的设计张力。

**坏消息五幕剧**：将用户期望落空的场景重构为五幕式情感交互（通知 → 共情 → 解释 → 行动 → 闭环），72 小时后主动回访是整个设计最关键的一笔。

**三序取舍原则**：用户自主 > 系统建议 > 商业目标。Agent 的任何一次发言违反此顺序，都视为设计失败。

**禁区锚点 + 未完待续锚点**：记忆中最微妙的两个维度——用户明示「不要碰」的区域和上次对话留下的开放钩子。市面 AI 产品尚无真正做好这两个维度。

## 章节速览

| 章节 | 主题 | 一句话 |
|------|------|--------|
| [01](docs/01-three-layer-memory.md) | 三层记忆架构 | 让 Agent「开箱即懂你」而不产生「被监控感」 |
| [02](docs/02-three-order-principle.md) | 三序取舍原则 | 用户意愿、系统建议、商业目标冲突时的排序铁律 |
| [03](docs/03-bad-news-five-acts.md) | 坏消息五幕剧 | 将最冷漠的拒绝场景重构为有温度的交互 |
| [04](docs/04-tri-modal-emotion.md) | 三模态情绪表达 | 动作 + 表情 + 文字，文字 AI 无法复制的护城河 |
| [05](docs/05-relationship-growth.md) | 关系成长体系 | 让用户愿意持续投入与 Agent 的关系 |
| [06](docs/06-memory-anchors.md) | 禁区锚点 + 未完待续锚点 | 市面 AI 尚无做好的两个记忆维度 |

## 已落地案例

### [花小呗｜支付宝花呗 AI 助手](cases/huaxiaobei/)

首个完整实例。以花呗 AI 助手「花小呗」为载体，完整落地 6 章设计原则。包含 4 个可交互 Demo 页面（智能对话 / 亲密度 / 小本本 / 拒额五幕剧）。

👉 [在线 Demo](https://keyuchen-del.github.io/Emotional-Companion-Agent/cases/huaxiaobei/)

## 版本

当前版本 **v0.1.0** — 首个 case 落地

查看 [CHANGELOG](CHANGELOG.md) | [Releases](https://github.com/keyuchen-del/Emotional-Companion-Agent/releases)

## License

[MIT](LICENSE)

## 作者

**Jacky（陈柯宇）**

北京大学汇丰商学院 金融硕士在读

---

*方案围绕一个用户可感知的终点展开：合上手机时，心里蹦出一句「TA 懂我」。*
