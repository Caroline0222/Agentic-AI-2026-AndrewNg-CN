# Module 1 · 章节速查索引

> 完整正文见 [README.md](./README.md)（聚焦 Introduction to Agentic Workflows）。
> 反思 / 工具 / 规划 / 多智能体 / 评测的详细草稿已存至 [notes/L2-L6-后续模块草稿.md](./notes/L2-L6-后续模块草稿.md)，供后续模块使用。

---

## 三十秒版

| 问题 | 答案 |
| --- | --- |
| Agentic 是什么？ | 把一件事拆成小步骤，中途加检查点再继续 |
| 有哪四种模式？ | 反思（自己查）、工具（连外部）、规划（先拆）、多智能体（分工）——详见 Module 2–5 |
| 从哪开始？ | **最简单的方案**，复杂度要靠评测证明值得 |
| 谁决定下一步？ | 代码规定 = workflow；模型决定 = agent |

---

## 目录导航

| 节 | 主题 | 关键结论 |
| --- | --- | --- |
| **一** | Agentic Workflow：多步骤工作流 | 核心是多步骤、可迭代的执行方式；HumanEval 95.1% 是最高值（up to） |
| **二** | 任务分解（Task Decomposition） | 每步有明确职责、能独立判断质量；错误易定位、可局部重试 |
| **三** | 自主度（Degrees of Autonomy） | 一条连续光谱，是一组授权；由业务风险与价值决定 |
| **四** | 四种设计模式 | 先掌握"什么时候用"，详细在 Module 2–5 |
| **五** | 为什么值得 | 扩大任务边界 + 五个场景判断问题 |
| **六** | Evals 与错误分析 | 靠闭环数据，评估业务结果 |
| **七** | 落地方法 | 从业务流程出发，先定起点再选实现 |
| **八** | 办公椅投标 | 贯穿案例：多步骤、需外部信息、值得迭代 |
| **小结** | 本节小结 | 可直接引用的 10 条观点 |

---

## 本篇最容易被搞错的四个事实

1. **单次生成 ≠ Zero-shot。** 前者描述调用方式，后者描述提示里有没有示例，二者不是同义词。
2. **HumanEval 的 95.1% 是"最高"（up to）。** 它来自 agentic 工作流多次调用的最优结果，不是等成本比较。
3. **workflow 与 agent 的区别看"谁做决定"。** 代码写死路径 = workflow；模型动态选步骤 = agent。跟"谁的模型更聪明"无关。
4. **自主程度不是开关，是一组授权。** 同一个业务里，不同环节可以采用不同程度的自主性。

---

## 配套资产

```
assets/
├── reflection_demo.py          # 代码示例（含反思/工具/规划/多智能体/评测 demo）
└── diagrams/                   # Mermaid 图源
chapters/module-01-introduction/
├── README.md                   # Module 1 成稿（Introduction）
├── README-index.md             # 本文件
└── notes/
    └── L2-L6-后续模块草稿.md     # 后续模块素材
```

---

## 引用来源

1. Andrew Ng, "How Agents Can Improve LLM Performance"（The Batch）— <https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance>
2. Anthropic, "Building Effective Agents" — <https://www.anthropic.com/research/building-effective-agents>
3. Andrew Ng, "Agentic AI"（DeepLearning.AI 课程）— <https://www.deeplearning.ai/courses/agentic-ai>

---

**下一章**：Module 2 · Reflection 反思
