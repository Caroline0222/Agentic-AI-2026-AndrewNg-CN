# Agentic AI × 人机交互 (HCI) 实践专栏

> 基于吴恩达《Agentic AI》课程（2026.8）的深度拆解，面向 AI 产品经理、解决方案架构师、Agent 工程师与前端体验设计师。核心特色是「设计模式 × 工程实践 × 人机交互 (HCI)」三线交叉，中文主版并附英文术语括号（如：反思模式 Reflection）。

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
| **Module 1** | Introduction to Agentic Workflows —— 多步骤工作流与四种模式总览 | ✅ 已完稿 |
| **Module 2** | 反思模式 Reflection —— 让 AI 自己检查作业 | 📅 待开始 |
| **Module 3** | 工具使用 Tool Use —— 让 AI 联通真实世界 | 📅 待开始 |
| **Module 4** | 规划 Planning —— 让 AI 自己拆解大目标 | 📅 待开始 |
| **Module 5** | 多智能体 Multi-Agent —— 让 AI 之间协作 | 📅 待开始 |

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
│   ├── module-01-introduction/        # Module 1：Introduction to Agentic Workflows
│   │   ├── README.md                  # 成稿
│   │   ├── README-index.md            # 速查索引
│   │   └── notes/                     # 后续模块素材草稿
│   ├── module-02-reflection/          # Module 2：Reflection（反思）
│   ├── module-03-tool-use/            # Module 3：Tool Use（工具使用）
│   ├── module-04-planning/            # Module 4：Planning（规划）
│   └── module-05-multi-agent/         # Module 5：Multi-Agent（多智能体）
└── assets/
    └── diagrams/                      # Mermaid 源文件 + 导出图
```

---

## 📜 License

MIT —— 内容欢迎转载学习，注明来源即可。
