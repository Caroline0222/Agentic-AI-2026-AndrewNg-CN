# Agentic AI × 人机交互 (HCI) 实践专栏

> 基于吴恩达 (Andrew Ng) 2026.8 最新版《Agentic AI》课程的深度拆解。
> 融合 2026 年 AWS Bedrock AgentCore、Google Cloud Vertex AI Agent Builder、Anthropic Claude 智能体接口设计等大厂工程实践。
> 每一章都落到"Agent 执行该模式时，前端 UI 该怎么呈现、如何建立用户信任"。

---

## 🎯 专栏定位

| 维度 | 说明 |
|---|---|
| **目标读者** | AI 产品经理、解决方案架构师、Agent 工程师、前端体验设计师 |
| **核心特色** | 设计模式 × 工程实践 × 人机交互 (HCI)，三者交叉 |
| **语言策略** | 中文主版 + 英文术语括号 (例如：反思模式 Reflection) |
| **图表** | Mermaid (GitHub 原生渲染) |
| **代码** | Python + LiteLLM，最小可运行示例 |
| **更新节奏** | 按 Module 推进，每完成一章提交一次 |

---

## 📚 课程底层逻辑

Andrew Ng 在 2026.8 这版课程里，把 Agentic AI 抽象成 **4 大设计模式**：

1. **反思 Reflection**：让 AI 自己检查作业
2. **工具使用 Tool Use**：让 AI 会调用外部 API/工具
3. **规划 Planning**：让 AI 拆解目标、子目标、执行、回溯
4. **多智能体 Multi-Agent**：让 AI 之间协作 / 对抗 / 分工

每一模式都有**底层逻辑 → 架构示意 → HCI 落点 → 代码示例 → 实战映射 → 面试表达**六层剖面。

---

## 🗺️ 5 章路线图（持续更新）

| Module | 主题 | 状态 |
|---|---|---|
| **Module 1** | 反思模式 Reflection —— 让 AI 自己检查作业 | 🔄 整理中 |
| **Module 2** | 工具使用 Tool Use —— 让 AI 联通真实世界 | 📅 待开始 |
| **Module 3** | 规划 Planning —— 让 AI 自己拆解大目标 | 📅 待开始 |
| **Module 4** | 多智能体 Multi-Agent —— 让 AI 之间协作 | 📅 待开始 |
| **Module 5** | 综合实战 —— 端到端 Agent 应用构建 | 📅 待开始 |

完整课程大纲见 [docs/ROADMAP.md](./docs/ROADMAP.md)。

---

## 📂 仓库结构

```
.
├── README.md                          # 本文件
├── LICENSE                            # MIT
├── .gitignore                         # Python/IDE 忽略
├── docs/
│   └── ROADMAP.md                     # 5 章完整目录大纲
├── chapters/
│   ├── README.md                      # 章节索引
│   ├── module-01-reflection/          # Module 1 工作目录
│   │   ├── README.md                  # 当前进度占位
│   │   └── notes/                     # 原始看课笔记
│   ├── module-02-tool-use/            # 待创建
│   ├── module-03-planning/            # 待创建
│   ├── module-04-multi-agent/         # 待创建
│   └── module-05-capstone/            # 待创建
└── assets/
    └── diagrams/                      # Mermaid 源文件 + 导出图
```

---

## ✍️ 作者与协作

- **共同作者**：Caroline He（港，软通动力方案顾问 / 智慧城市 AI Agent FDE）
- **AI Co-author**：WorkBuddy Agent
- **协作方式**：每看完一个 Module，把原始笔记贴给 AI Co-author，
  AI 整合课程原意 + 2026 大厂调研 + 实战映射，输出成稿；
  人类 Review 后定稿，再 push。

---

## 📜 License

MIT —— 内容欢迎转载学习，注明来源即可。
