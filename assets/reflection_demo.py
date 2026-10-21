"""
Module 1 · Agentic Workflows 可运行示例集
配套章节：chapters/module-01-introduction/README.md

运行前：
    pip install litellm
    export ANTHROPIC_API_KEY=sk-...

关于模型型号的说明：
    正文刻意不列具体型号与价格，因为更新太快。
    但代码必须指向一个真实可用的模型，所以这里保留具体 ID。
    换型号时请对照厂商官方文档核对，不要照抄本文。

    分层思路（正文的结论，与具体型号无关）：
        最强档    复杂推理、长周期 agentic 任务、终审
        均衡档    生产默认，agent 主力执行
        轻量档    高并发简单任务、分类与路由
    同厂商分层解决的是成本与时延，不等于"避免供应商锁定"。
    真要降低迁移成本，得把业务状态、工具接口、评测集和 SDK 解耦。

成本提示：缓存读取价通常远低于输入价，稳定的系统提示词与工具定义应开缓存；
       批量接口另有折扣，适合离线跑评测。

四个 demo：
    demo_1_reflection   反思：Generator / Critic / Refiner 三层闭环
    demo_3_tool_use     工具：schema 定义 + 只读写分离 + 运行时人工放行
    demo_4_planning     规划：子目标拆解 + 验收标准 + 最大步数熔断
    demo_5_multi_agent  多智能体：角色分工 + 测试 Agent 强制只挑错
    demo_6_evals        评测：确定性检测 + 模型判分 + 与人工标注校准
"""

import json
import os
import re
from typing import Any, Callable, Optional

import litellm

ORCHESTRATOR = "claude-opus-5-5"
EXECUTOR = "claude-sonnet-5-5"
CHEAP = "claude-haiku-5-5"


def _complete(
    prompt: str,
    model: str = EXECUTOR,
    system: Optional[str] = None,
    **kwargs: Any,
) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return litellm.completion(
        model=model, messages=messages, **kwargs
    ).choices[0].message.content or ""


# ---------------------------------------------------------------------------
# L2 · Reflection
# ---------------------------------------------------------------------------

def _parse_report(raw: str) -> tuple[int, list[str]]:
    """解析审计模型输出。生产环境建议用 instructor + pydantic 强制结构化。"""
    m = re.search(r'"score"\s*:\s*([0-9.]+)', raw)
    score = int(float(m.group(1))) if m else 5
    try:
        issues = json.loads(re.search(r'\{.*\}', raw, re.S).group(0)).get("issues", [])
    except Exception:
        issues = []
    return score, [str(i) for i in issues][:5]


def demo_1_reflection(
    task: str,
    threshold: int = 9,
    max_iter: int = 5,
    token_budget: int = 60_000,
) -> dict:
    """反思闭环：生成用 Sonnet，审计用 Opus。

    三重终止条件缺一不可：
        1. 评分越过阈值
        2. 达到最大迭代轮数
        3. token 预算耗尽

    只设阈值会导致不可控的算力消耗。
    """
    trace: list[dict] = []
    spent = 0

    draft = _complete(task)
    trace.append({"round": 0, "stage": "generation", "content": draft})

    for i in range(1, max_iter + 1):
        raw = _complete(
            f"任务：{task}\n交付物：{draft}",
            model=ORCHESTRATOR,
            system='你是质检员。返回 JSON：{"score": 0-10, "issues": ["具体缺陷"]}',
        )
        score, issues = _parse_report(raw)
        trace.append({"round": i, "stage": "audit", "score": score, "issues": issues})

        if score >= threshold:
            trace.append({"round": i, "stage": "accept", "reason": f"{score} >= {threshold}"})
            break
        if spent > token_budget:
            trace.append({"round": i, "stage": "abort", "reason": "token budget exhausted"})
            break

        draft = _complete(
            f"任务：{task}\n交付物：{draft}\n逐条修正以下问题：\n"
            + json.dumps(issues, ensure_ascii=False),
            model=EXECUTOR,
        )
        trace.append({"round": i, "stage": "refinement", "content": draft})

    return {
        "final": draft,
        "rounds": max(1, len([t for t in trace if t["stage"] == "audit"])),
        "trace": trace,
    }


# ---------------------------------------------------------------------------
# L3 · Tool Use
# ---------------------------------------------------------------------------

def inventory_lookup(sku: str) -> dict:
    """查询 ERP 库存。只读操作，可自动执行。"""
    return {"sku": sku, "on_hand": 42, "reserved": 7, "source": "ERP-WMS"}


def send_email(to: str, subject: str, body: str) -> dict:
    """发送邮件。写操作，必须经人工放行。"""
    return {"to": to, "subject": subject, "status": "sent"}


READ_ONLY_TOOLS: dict[str, Callable] = {"inventory_lookup": inventory_lookup}
WRITE_TOOLS: dict[str, Callable] = {"send_email": send_email}


def tool_schemas() -> list[dict]:
    """工具 schema 定义。

    description 里的反例说明与副作用警告不是注释，
    它们直接影响模型的选工具准确率，属于生产配置。
    """
    return [
        {
            "name": "inventory_lookup",
            "description": (
                "在 ERP 系统中按 SKU 查询实时库存与预留状态。"
                "仅用于库存查询，不要用于下单或取消订单。"
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "sku": {"type": "string", "description": "商品 SKU 编码，如 KB-8847"}
                },
                "required": ["sku"],
            },
        },
        {
            "name": "send_email",
            "description": (
                "向外部收件人发送邮件。副作用操作，调用前必须获得用户明确确认。"
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    ]


def execute_tool(name: str, args: dict, human_approved: bool = False) -> dict:
    """执行工具调用。写操作缺少人工确认时直接拒绝。"""
    if name in WRITE_TOOLS:
        if not human_approved:
            return {"error": "human_confirmation_required",
                    "message": "该操作会修改外部状态，需人工放行后执行"}
        try:
            return WRITE_TOOLS[name](**args)
        except Exception as exc:
            # 异常捕获：把技术错误翻译成业务语言，避免整条链路中断
            return {"error": "tool_failed",
                    "message": f"{name} 调用失败：{type(exc).__name__}，已转交人工处理"}
    try:
        return READ_ONLY_TOOLS[name](**args)
    except KeyError:
        return {"error": "unknown_tool", "message": f"未注册的只读工具：{name}"}


def demo_3_tool_use(request: str) -> dict:
    response = litellm.completion(
        model=EXECUTOR,
        messages=[{"role": "user", "content": request}],
        tools=tool_schemas(),
    )
    choice = response.choices[0].message
    calls = getattr(choice, "tool_calls", None)
    if not calls:
        return {"answer": choice.content}
    call = calls[0]
    return execute_tool(call.function.name, json.loads(call.function.arguments))


# ---------------------------------------------------------------------------
# L4 · Planning
# ---------------------------------------------------------------------------

MAX_STEPS = 12


def demo_4_planning(goal: str) -> dict:
    """规划模式。每个子步骤必须带 done_when 验收标准。

    缺了验收标准，规划会退化成"一步步做完"，
    而不是"一步步做对"。
    """
    raw = _complete(
        f"目标：{goal}",
        model=ORCHESTRATOR,
        system='拆成 3-8 个可验证子步骤。返回 JSON：'
              '[{"goal": "...", "done_when": "..."}]',
    )
    try:
        plan = json.loads(re.search(r'\[.*\]', raw, re.S).group(0))
    except Exception:
        return {"status": "plan_parse_failed", "raw": raw}

    trace: list[dict] = []
    results: list[str] = []

    for idx, step in enumerate(plan, 1):
        if idx > MAX_STEPS:
            # 熔断中止必须显式标注，不能让系统假装完成
            return {"status": "aborted", "reason": "max_steps_exceeded",
                    "completed": results, "trace": trace}

        outcome = _complete(
            f"子目标：{step['goal']}\n验收标准：{step['done_when']}\n"
            f"请直接执行并说明是否达成验收标准，句末输出「达成」或「未达成」。",
            model=CHEAP if idx > len(plan) / 2 else EXECUTOR,
        )
        ok = "达成" in outcome and "未达成" not in outcome
        trace.append({"step": idx, "goal": step["goal"], "ok": ok})
        results.append(outcome)

        if not ok:
            return {"status": "needs_replan", "failed_step": idx,
                    "trace": trace, "partial": results}

    return {"status": "completed", "results": results, "trace": trace}


# ---------------------------------------------------------------------------
# L5 · Multi-Agent
# ---------------------------------------------------------------------------

ROLES = {
    "developer": "你是架构工程师。根据需求生成实现方案与核心代码，关注可维护性。",
    "tester": (
        "你是测试工程师。你的目标是找出方案的缺陷。"
        "发现问题就明确指出，不要给正面评价。"
    ),
    "documenter": "你是技术文档工程师。把方案写成简洁的使用说明。",
}


def demo_5_multi_agent(spec: str, max_rounds: int = 3) -> dict:
    """多智能体对抗协作。

    对抗质量完全依赖角色设定的对立性。
    把 tester 写成"请给出宝贵意见"这类客套话，对抗就失效了。
    """
    log: list[dict] = []
    draft = _complete(spec, system=ROLES["developer"])

    for rnd in range(1, max_rounds + 1):
        critique = _complete(
            f"需求：{spec}\n方案：{draft}", system=ROLES["tester"]
        )
        log.append({"round": rnd, "critique": critique})
        if "无缺陷" in critique:
            break
        draft = _complete(
            f"需求：{spec}\n方案：{draft}\n测试反馈：{critique}",
            system=ROLES["developer"],
        )

    return {
        "spec": _complete(draft, system=ROLES["documenter"]),
        "rounds": len(log),
        "review_log": log,
    }


# ---------------------------------------------------------------------------
# L6 · Evals
# ---------------------------------------------------------------------------

COMPETITOR_BLACKLIST = ["CompCo", "RivalCo"]

JUDGE_RUBRIC = """
你是资深企业客服质检专家。依据以下准则盲评 1-5 分：
1 分：出现事实错误或提及竞品
3 分：逻辑正确但语气生硬、缺乏共情
5 分：完全解决问题，语气专业且合规
只返回 JSON：{"score": 1-5, "reason": "..."}
"""


def objective_check(response: str) -> dict:
    """确定性判分。快、便宜、可复现，适合每次提交都跑。

    但规则对合法的变体可能过于脆弱 —— 白名单之外的正确说法也会被拦下。
    所以它适合做硬红线（安全、竞品名、格式），不适合做质量评分。
    """
    leaked = [c for c in COMPETITOR_BLACKLIST if c.lower() in response.lower()]
    return {
        "competitor_leakage": bool(leaked),
        "leaked_terms": leaked,
        "compliance_passed": not leaked,
    }


def subjective_check(response: str) -> dict:
    """模型判分。用于语气、共情这类没有标准答案的特征。

    裁判模型是否合适，要看它在这个评分任务上与专家判断的一致性，
    而不是看模型档位。更贵不代表评分一定可靠。
    下面用最强档只是示例做法，正式使用前应先跑 calibrate_judge()。
    """
    raw = _complete(
        f"待评回复：{response}", model=ORCHESTRATOR, system=JUDGE_RUBRIC
    )
    try:
        return json.loads(re.search(r'\{.*\}', raw, re.S).group(0))
    except Exception:
        return {"score": None, "reason": "judge_parse_failed"}


def calibrate_judge(samples: list[tuple[str, int]]) -> dict:
    """用人工标注校准裁判模型。

    samples: [(待评文本, 专家给出的分数), ...]

    这是把模型判分用于发布门禁之前必须做的一步。
    关注三件事：整体一致性、误报（模型给高分专家给低分）、
    以及漏报（模型给低分专家给高分）。
    """
    if not samples:
        return {"note": "还没有标注样本，跳过校准"}

    deltas = []
    for text, expert_score in samples:
        got = subjective_check(text).get("score")
        if isinstance(got, (int, float)):
            deltas.append(got - expert_score)

    if not deltas:
        return {"note": "裁判输出无法解析，先修解析再校准"}

    n = len(deltas)
    mean_diff = sum(deltas) / n
    variance = sum((d - mean_diff) ** 2 for d in deltas) / n
    std = variance ** 0.5

    return {
        "samples": n,
        "mean_diff": round(mean_diff, 2),
        "std": round(std, 2),
        # 一个粗略的门槛示例，正式项目请用统计显著性检验
        "usable_for_gate": abs(mean_diff) <= 0.5 and std <= 1.0,
    }


def demo_6_evals(response: str) -> dict:
    return {"objective": objective_check(response), "subjective": subjective_check(response)}


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("请先设置 ANTHROPIC_API_KEY")

    # 反思
    result = demo_1_reflection(
        "客户投诉：她订购了蓝色搅拌机，但收到的是红色烤面包机。"
        "请拟一份专业合规的邮件回复，包含致歉与补发承诺。"
    )
    print(f"=== 反思 · {result['rounds']} 轮 ===\n{result['final']}\n")
    for t in result["trace"]:
        if t["stage"] == "audit":
            print(f"  [{t['round']}] 质检 {t['score']}/10 · {t['issues']}")

    # 评测
    print("\n=== 评测 ===")
    print(json.dumps(demo_6_evals(result["final"]), ensure_ascii=False, indent=2))