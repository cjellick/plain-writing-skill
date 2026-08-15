#!/usr/bin/env python3
"""Write evals/README.md from the latest output summaries and samples."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "dataset.jsonl"
README = ROOT / "README.md"
FABLE_OUT = ROOT / "outputs" / "fable_coding"
NEW_RULES_OUT = ROOT / "outputs" / "new_rules"
SAMPLE_IDS = ("51", "54", "57")
EXCERPT_CHARS = 900


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def load_dataset() -> dict[str, dict]:
    items = {}
    with DATASET.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            items[item["id"]] = item
    return items


def wrapup_from_prompt(prompt: str) -> str:
    marker = "Wrap-up:\n"
    if marker not in prompt:
        return ""
    return prompt.split(marker, 1)[1].strip()


def excerpt(text: str, limit: int = EXCERPT_CHARS) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n[...]"


def pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.0f}%"


def summary_table(summary: dict) -> str:
    return "\n".join(
        [
            "| Metric | Result |",
            "| --- | --- |",
            f"| Items | {summary.get('n', 0)} |",
            f"| Skill wins / baseline wins / ties | {summary.get('skill_wins', 0)} / {summary.get('baseline_wins', 0)} / {summary.get('ties', 0)} |",
            f"| Item win rate among decisive | {pct(summary.get('skill_win_rate_among_decisive'))} |",
            f"| Criterion skill / baseline / tie | {summary.get('criterion_skill_wins', 0)} / {summary.get('criterion_baseline_wins', 0)} / {summary.get('criterion_ties', 0)} |",
            f"| Criterion win rate among decisive | {pct(summary.get('criterion_skill_win_rate_among_decisive'))} |",
            f"| Errors | {summary.get('errors', 0)} |",
            f"| Rewriter / judge | {summary.get('model', '?')} / {summary.get('judge_model', '?')} |",
        ]
    )


def criterion_rows(summary: dict, limit: int = 8) -> str:
    by_c = summary.get("by_criterion") or {}
    rows = []
    for key, bucket in by_c.items():
        decisive = bucket.get("skill_wins", 0) + bucket.get("baseline_wins", 0)
        if not decisive:
            continue
        rows.append(
            (
                bucket.get("skill_win_rate_among_decisive") or 0,
                bucket.get("id"),
                bucket.get("title"),
                bucket.get("skill_wins", 0),
                bucket.get("baseline_wins", 0),
                bucket.get("ties", 0),
            )
        )
    rows.sort(key=lambda r: (-(r[3] - r[4]), -r[3], r[1]))
    lines = [
        "| Rule | Skill / baseline / tie | Skill win rate |",
        "| --- | --- | --- |",
    ]
    for rate, cid, title, sw, bw, ties in rows[:limit]:
        lines.append(f"| {cid}. {title} | {sw} / {bw} / {ties} | {pct(rate)} |")
    losses = [r for r in rows if r[4] > r[3]]
    if losses:
        lines.extend(["", "Rules where the baseline won more often:", ""])
        lines.extend(
            [
                "| Rule | Skill / baseline / tie | Skill win rate |",
                "| --- | --- | --- |",
            ]
        )
        for rate, cid, title, sw, bw, ties in losses[:5]:
            lines.append(f"| {cid}. {title} | {sw} / {bw} / {ties} | {pct(rate)} |")
    return "\n".join(lines)


def fable_sample(item_id: str, dataset: dict[str, dict], out_dir: Path) -> str:
    row = load_json(out_dir / f"{item_id}.json")
    item = dataset.get(item_id)
    if not row or not item:
        return f"No sample for item {item_id}."
    source = item.get("source") or {}
    task = source.get("task", item_id)
    wrapup = wrapup_from_prompt(item.get("prompt") or "")
    judgment = row.get("judgment") or {}
    return "\n".join(
        [
            f"### Item {item_id}: `{task}`",
            "",
            f"Judge: skill_better={judgment.get('skill_better')} "
            f"({judgment.get('skill_criteria_wins')}-"
            f"{judgment.get('baseline_criteria_wins')}-"
            f"{judgment.get('criteria_ties')}).",
            "",
            "Original wrap-up:",
            "",
            "```",
            excerpt(wrapup),
            "```",
            "",
            "Baseline rewrite:",
            "",
            "```",
            excerpt(row.get("baseline") or ""),
            "```",
            "",
            "Rewrite with the skill:",
            "",
            "```",
            excerpt(row.get("with_skill") or ""),
            "```",
        ]
    )


def main() -> None:
    dataset = load_dataset()
    fable_summary = load_json(FABLE_OUT / "summary.json")
    new_rules_summary = load_json(NEW_RULES_OUT / "summary.json")

    parts = [
        "# Plain-writing evals",
        "",
        "These evals ask whether giving `SKILL.md` to a writer produces text that",
        "follows the plain-writing rules better than a writer that does not see",
        "the skill.",
        "",
        "## Eval procedure",
        "",
        "Each item in `dataset.jsonl` is one writing task. Some items are a short",
        "prompt only. History items also load a conversation from",
        "`evals/sources/` and append the item prompt as the last user turn.",
        "",
        "The fable items (`51`–`65`) load a full Claude Fable 5 coding-agent",
        "trace. The prompt quotes the longest text-only assistant wrap-up from",
        "that trace and asks the model to rewrite it. The rest of the trace stays",
        "in the history so the writer can use it.",
        "",
        "For every item, the same user messages are sent twice.",
        "",
        "First, a baseline writer gets a short system prompt that only asks for a",
        "clear, complete response. Second, a skill writer gets the full text of",
        "`SKILL.md` and is told to follow it. Both writers use the same model.",
        "Neither writer sees the other output.",
        "",
        "A judge then compares the two outputs. The numbered rules in `SKILL.md`",
        "are the criteria. For each rule, the judge sees the task prompt, text A,",
        "and text B. The A and B labels are shuffled at random so the judge does",
        "not know which text came from the skill. The judge scores only that one",
        "rule and returns `a`, `b`, or `tie`. Before and after examples are",
        "stripped from the rule text before it is sent.",
        "",
        "An item counts as a skill win when the skill text wins more rules than",
        "the baseline. It counts as a baseline win when the baseline wins more",
        "rules. Equal rule counts are a tie. The summary also adds up wins at the",
        "rule level across items.",
        "",
        "The default rewriter and judge are `gpt-5.5`. You can change them with",
        "`--model` and `--judge-model`.",
        "",
        "## How to run",
        "",
        "```",
        "uv sync",
        "uv run python evals/run_eval.py",
        "uv run python evals/run_eval.py --category fable_coding",
        "uv run python evals/run_eval.py --ids 66,67",
        "uv run python evals/write_readme.py",
        "```",
        "",
        "Put `OPENAI_API_KEY` in a `.env` file at the repo root. Outputs land in",
        "`evals/outputs/` and are gitignored. This README is updated from those",
        "outputs by `write_readme.py`.",
        "",
        "## Dataset",
        "",
        f"There are {len(dataset)} items in `dataset.jsonl`.",
        "",
        "- `01`–`40`: short prompts, public-domain excerpts, and LLM slop.",
        "- `41`–`50`: long research and support-agent histories.",
        "- `51`–`65`: long Claude Fable 5 coding-agent traces. The model sees the",
        "  full trace and rewrites the longest wrap-up.",
        "- `66`–`67`: chat context and lists-or-tables checks.",
        "",
        "Fable traces are rebuilt with `uv run python evals/build_fable_histories.py`.",
        "",
    ]

    if fable_summary:
        parts.extend(
            [
                "## Latest fable coding results",
                "",
                "Category `fable_coding`, items `51`–`65`. The rewriter gets the full",
                "trace and the longest wrap-up. The judge compares the baseline rewrite",
                "to the skill rewrite on each writing rule.",
                "",
                summary_table(fable_summary),
                "",
                "Rules with the largest gap:",
                "",
                criterion_rows(fable_summary),
                "",
                "## Fable before and after",
                "",
                "Each sample is the original longest wrap-up, the baseline rewrite, and",
                "the rewrite with the skill. Long texts are cut after about 900 characters.",
                "",
            ]
        )
        samples = [fable_sample(item_id, dataset, FABLE_OUT) for item_id in SAMPLE_IDS]
        parts.append("\n\n".join(samples))
        parts.append("")
    else:
        parts.extend(
            [
                "## Latest fable coding results",
                "",
                "No `evals/outputs/fable_coding/summary.json` yet. Run",
                "`uv run python evals/run_eval.py --category fable_coding` and then",
                "`uv run python evals/write_readme.py`.",
                "",
            ]
        )

    if new_rules_summary:
        parts.extend(
            [
                "## Latest items 66 and 67",
                "",
                "These two prompts check the chat-context rule and the lists-or-tables rule.",
                "",
                summary_table(new_rules_summary),
                "",
            ]
        )

    README.write_text("\n".join(parts).rstrip() + "\n")
    print(f"Wrote {README}")


if __name__ == "__main__":
    main()
