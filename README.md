# Agentic AI 学习笔记

基于 Andrew Ng《Agentic AI》课程（DeepLearning.AI, 2026.8）整理的中文笔记。课程把 Agentic AI 拆成 4 种设计模式，配上评估、错误分析、成本优化等工程实践方法。这里按模块逐节整理，中文为主，关键术语附英文。

面向在做 Agent 项目的方案架构师、产品经理和工程师。

## 四种设计模式

| 模式 | 解决什么 | 对应模块 |
|---|---|---|
| Reflection（反思） | 首次结果不够好，需要检查和修订 | Module 2 |
| Tool Use（工具使用） | 模型缺乏信息或执行能力 | Module 3 |
| Planning（规划） | 步骤复杂，需要动态拆解和执行 | Module 5 |
| Multi-Agent（多智能体） | 单个 Agent 职责过多，需要分工协作 | Module 5 |

Module 1 是总览，Module 4 是工程实践（评估 / 错误分析 / 组件级评估 / 改进方法 / 成本延迟优化 / 开发流程）。

## 5 章路线图

| Module | 主题 | 涵盖内容 | 状态 |
|---|---|---|---|
| Module 1 | Introduction to Agentic Workflows | 多步骤工作流、任务分解、自主度光谱、四种模式总览、Evals 入门、落地方法 | ✅ |
| Module 2 | Reflection | 反思流程、检查标准与模型分工、外部反馈、图表多模态评审、评估方法、停止条件、国内工程实践 | ✅ |
| Module 3 | Tool Use | 工具定义与执行流程、手动提示工程与原生 Function Calling、AI Suite 语法、代码执行、MCP 协议 | ✅ |
| Module 4 | Practical Tips | Evals 评估体系、错误分析、组件级评估、改进方法（提示词/换模型/任务分解/微调）、成本与延迟优化、开发流程闭环 | ✅ |
| Module 5 | Patterns for Highly Autonomous Agents | Planning 设计模式、结构化输出、代码作为行动、Multi-Agent 系统、通信模式（线性/双层/多层/去中心） | ✅ |

## 仓库结构

```
chapters/
├── module-01-introduction/      3 篇（1.1–1.3）
├── module-02-reflection/        5 篇（2.1–2.5）
├── module-03-tool-use/          5 篇（3.1–3.5）
├── module-04-practical-tips/    7 篇（4.1–4.7）
└── module-05-multi-agent/       5 篇（5.1–5.5）
```

共 25 篇笔记，每篇独立 .md 文件。完整目录见 [chapters/README.md](./chapters/README.md)。

## 约定

- 语言：中文为主，关键术语附英文（如：反思模式 Reflection）
- 图表：Mermaid 内联代码块，GitHub 原生渲染
- 数据：量化数据标注出处，benchmark 注明基准名称与测试条件
- 脱敏：客户名称、合同金额、可识别的商业信息一律打码

## License

MIT
