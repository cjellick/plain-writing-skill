#!/usr/bin/env python3
"""Write evals/README.md from the latest output summaries and samples."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "dataset.jsonl"
README = ROOT / "README.md"
OUTPUTS = ROOT / "outputs"
RESULT_DIRS = (
    OUTPUTS / "core",
    OUTPUTS / "fable_coding",
    OUTPUTS / "new_rules",
    OUTPUTS / "all",
)
EXCERPT_CHARS = 900
TRACKS = (
    {
        "title": "Short tasks",
        "ids": tuple(f"{i:02d}" for i in range(1, 41)),
        "blurb": "Items `01`–`40`: LLM slop, public-domain excerpts, and short drafts.",
    },
    {
        "title": "Long history",
        "ids": tuple(f"{i:02d}" for i in range(41, 51)),
        "blurb": "Items `41`–`50`: research and support-agent histories.",
    },
    {
        "title": "Fable coding",
        "ids": tuple(f"{i:02d}" for i in range(51, 66)),
        "blurb": "Items `51`–`65`: Claude Fable 5 coding-agent traces. The writer sees the full trace and rewrites the longest wrap-up.",
    },
    {
        "title": "Chat and lists",
        "ids": ("66", "67"),
        "blurb": "Items `66`–`67`: chat context and short-list checks.",
    },
)
SAMPLES = (
    ("01", "Deslopify"),
    ("12", "Public-domain rewrite"),
    ("22", "Short draft"),
    ("41", "Long history"),
    ("51", "Fable coding"),
    ("66", "Chat context"),
    ("67", "Short lists"),
)


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


def load_results() -> dict[str, dict]:
    """Load per-item result files. Later dirs override earlier ones."""
    results: dict[str, dict] = {}
    for out_dir in RESULT_DIRS:
        if not out_dir.is_dir():
            continue
        for path in sorted(out_dir.glob("[0-9][0-9].json")):
            row = load_json(path)
            if row and row.get("id"):
                results[row["id"]] = row
    return results


def raw_text(item: dict) -> str | None:
    prompt = item.get("prompt") or ""
    for marker in ("Wrap-up:\n", "Text:\n", "Excerpt:\n"):
        if marker in prompt:
            return prompt.split(marker, 1)[1].strip()
    return None


def excerpt(text: str, limit: int = EXCERPT_CHARS) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n[...]"


def pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.0f}%"


def summarize(rows: list[dict]) -> dict:
    wins = sum(1 for r in rows if r.get("judgment", {}).get("skill_better") is True)
    losses = sum(1 for r in rows if r.get("judgment", {}).get("skill_better") is False)
    errors = sum(1 for r in rows if "error" in r)
    ties = len(rows) - wins - losses
    criterion_skill = sum(
        r.get("judgment", {}).get("skill_criteria_wins", 0) for r in rows
    )
    criterion_baseline = sum(
        r.get("judgment", {}).get("baseline_criteria_wins", 0) for r in rows
    )
    criterion_ties = sum(r.get("judgment", {}).get("criteria_ties", 0) for r in rows)
    models = {(r.get("model"), r.get("judge_model")) for r in rows}
    model = "?"
    judge = "?"
    if len(models) == 1:
        only = next(iter(models))
        model = only[0] or "?"
        judge = only[1] or "?"
    elif rows:
        # Item files do not store model; fall back to a sibling summary.
        model = rows[0].get("model") or "?"
        judge = rows[0].get("judge_model") or "?"
    return {
        "n": len(rows),
        "skill_wins": wins,
        "baseline_wins": losses,
        "ties": ties,
        "errors": errors,
        "skill_win_rate_among_decisive": (
            wins / (wins + losses) if (wins + losses) else None
        ),
        "criterion_skill_wins": criterion_skill,
        "criterion_baseline_wins": criterion_baseline,
        "criterion_ties": criterion_ties,
        "criterion_skill_win_rate_among_decisive": (
            criterion_skill / (criterion_skill + criterion_baseline)
            if (criterion_skill + criterion_baseline)
            else None
        ),
        "model": model,
        "judge_model": judge,
        "by_criterion": summarize_criteria(rows),
    }


def summarize_criteria(rows: list[dict]) -> dict:
    by_id: dict[int, dict] = {}
    for row in rows:
        for crit in row.get("judgment", {}).get("criteria") or []:
            cid = crit.get("id")
            if cid is None:
                continue
            bucket = by_id.setdefault(
                cid,
                {
                    "id": cid,
                    "title": crit.get("title") or str(cid),
                    "skill_wins": 0,
                    "baseline_wins": 0,
                    "ties": 0,
                },
            )
            if crit.get("title"):
                bucket["title"] = crit["title"]
            if crit.get("skill_better") is True:
                bucket["skill_wins"] += 1
            elif crit.get("skill_better") is False:
                bucket["baseline_wins"] += 1
            else:
                bucket["ties"] += 1
    return {
        str(cid): {
            **bucket,
            "skill_win_rate_among_decisive": (
                bucket["skill_wins"] / (bucket["skill_wins"] + bucket["baseline_wins"])
                if (bucket["skill_wins"] + bucket["baseline_wins"])
                else None
            ),
        }
        for cid, bucket in sorted(by_id.items())
    }


def attach_models(summary: dict, result_dirs: tuple[Path, ...]) -> dict:
    if summary.get("model") not in (None, "?"):
        return summary
    for out_dir in reversed(result_dirs):
        sibling = load_json(out_dir / "summary.json")
        if sibling and sibling.get("model"):
            summary["model"] = sibling.get("model", "?")
            summary["judge_model"] = sibling.get("judge_model", "?")
            return summary
    return summary


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


def track_table(results: dict[str, dict]) -> str:
    lines = [
        "| Track | Items | Skill / baseline / tie | Criterion skill / baseline / tie | Item win rate |",
        "| --- | --- | --- | --- | --- |",
    ]
    for track in TRACKS:
        rows = [results[i] for i in track["ids"] if i in results]
        if not rows:
            lines.append(
                f"| {track['title']} | 0 / {len(track['ids'])} | n/a | n/a | n/a |"
            )
            continue
        summary = summarize(rows)
        lines.append(
            "| {title} | {have} / {want} | {sw} / {bw} / {ties} | {csw} / {cbw} / {ct} | {rate} |".format(
                title=track["title"],
                have=len(rows),
                want=len(track["ids"]),
                sw=summary["skill_wins"],
                bw=summary["baseline_wins"],
                ties=summary["ties"],
                csw=summary["criterion_skill_wins"],
                cbw=summary["criterion_baseline_wins"],
                ct=summary["criterion_ties"],
                rate=pct(summary["skill_win_rate_among_decisive"]),
            )
        )
    return "\n".join(lines)


def category_table(results: dict[str, dict], dataset: dict[str, dict]) -> str:
    buckets: dict[str, list[dict]] = {}
    for item_id, row in results.items():
        category = row.get("category") or dataset.get(item_id, {}).get("category") or "?"
        buckets.setdefault(category, []).append(row)
    lines = [
        "| Category | Items | Skill / baseline / tie | Criterion skill / baseline / tie | Item win rate |",
        "| --- | --- | --- | --- | --- |",
    ]
    for category, rows in sorted(buckets.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        summary = summarize(rows)
        lines.append(
            "| `{cat}` | {n} | {sw} / {bw} / {ties} | {csw} / {cbw} / {ct} | {rate} |".format(
                cat=category,
                n=summary["n"],
                sw=summary["skill_wins"],
                bw=summary["baseline_wins"],
                ties=summary["ties"],
                csw=summary["criterion_skill_wins"],
                cbw=summary["criterion_baseline_wins"],
                ct=summary["criterion_ties"],
                rate=pct(summary["skill_win_rate_among_decisive"]),
            )
        )
    return "\n".join(lines)


def criterion_rows(summary: dict, limit: int = 8) -> str:
    by_c = summary.get("by_criterion") or {}
    rows = []
    for bucket in by_c.values():
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


def sample_block(item_id: str, label: str, dataset: dict[str, dict], row: dict) -> str:
    item = dataset.get(item_id) or {}
    source = item.get("source") or {}
    title = source.get("task") or source.get("title") or item.get("category") or item_id
    judgment = row.get("judgment") or {}
    lines = [
        f"### {label}: item {item_id} (`{title}`)",
        "",
        f"Judge: skill_better={judgment.get('skill_better')} "
        f"({judgment.get('skill_criteria_wins')}-"
        f"{judgment.get('baseline_criteria_wins')}-"
        f"{judgment.get('criteria_ties')}).",
        "",
    ]
    raw = raw_text(item)
    if raw:
        lines.extend(["Raw text:", "", "```", excerpt(raw), "```", ""])
    else:
        lines.extend(
            [
                "Task:",
                "",
                "```",
                excerpt(item.get("prompt") or row.get("prompt") or ""),
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "Baseline-rewritten:",
            "",
            "```",
            excerpt(row.get("baseline") or ""),
            "```",
            "",
            "Skill-based rewritten:",
            "",
            "```",
            excerpt(row.get("with_skill") or ""),
            "```",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    dataset = load_dataset()
    results = load_results()
    rows = [results[i] for i in dataset if i in results]
    overall = attach_models(summarize(rows), RESULT_DIRS) if rows else None

    parts = [
        "# Plain-writing evals",
        "",
        "These evals ask whether giving `SKILL.md` to a writer produces text that",
        "follows the plain-writing rules better than a writer that does not see",
        "the skill.",
        "",
        "## Eval procedure",
        "",
        "### Dataset",
        "",
        f"`dataset.jsonl` has {len(dataset)} writing tasks.",
        "",
        "- `01`–`40`: short prompts, public-domain excerpts, and LLM slop.",
        "- `41`–`50`: long research and support-agent histories.",
        "- `51`–`65`: Claude Fable 5 coding-agent traces. The writer sees the",
        "  full trace and is asked to rewrite the longest wrap-up.",
        "- `66`–`67`: chat context and short-list checks.",
        "",
        "History items load a conversation from `evals/sources/` and append the",
        "item prompt as the last user turn. Fable traces are rebuilt with",
        "`uv run python evals/build_fable_histories.py`.",
        "",
        "### Baseline",
        "",
        "The same user messages are sent to the writer with a short system prompt:",
        "write a clear, complete response, and return only the requested writing.",
        "The writer does not see `SKILL.md`.",
        "",
        "### Skill condition",
        "",
        "The same user messages are sent again, to the same model, with `SKILL.md`",
        "in the system prompt. The writer is told to follow those rules. It does",
        "not see the baseline output.",
        "",
        "### How it is judged",
        "",
        "A judge compares the two outputs on each numbered rule in `SKILL.md`.",
        "For each rule it sees the task prompt and two unlabeled texts, A and B.",
        "The labels are shuffled so the judge does not know which text used the",
        "skill. It returns `a`, `b`, or `tie` for that rule only.",
        "",
        "An item is a skill win if the skill text wins more rules than the",
        "baseline, a baseline win if the reverse is true, and a tie if the rule",
        "counts are equal. The summary also totals those rule wins across items.",
        "",
        "The default rewriter and judge are `gpt-5.5`. Override them with",
        "`--model` and `--judge-model`.",
        "",
        "## How to run",
        "",
        "```",
        "uv sync",
        "uv run python evals/run_eval.py --out evals/outputs/core",
        "uv run python evals/run_eval.py --category fable_coding --out evals/outputs/fable_coding",
        "uv run python evals/run_eval.py --ids 66,67 --out evals/outputs/new_rules",
        "uv run python evals/write_readme.py",
        "```",
        "",
        "Put `OPENAI_API_KEY` in a `.env` file at the repo root. Outputs land in",
        "`evals/outputs/` and are gitignored. This README is updated from those",
        "outputs by `write_readme.py`.",
        "",
    ]

    if overall:
        missing = [i for i in dataset if i not in results]
        parts.extend(
            [
                "## Latest results",
                "",
                f"Combined from `{len(results)}` of `{len(dataset)}` items.",
                "",
                summary_table(overall),
                "",
                "### By track",
                "",
                track_table(results),
                "",
                "### By category",
                "",
                category_table(results, dataset),
                "",
                "### Rules with the largest gap",
                "",
                criterion_rows(overall),
                "",
            ]
        )
        if missing:
            parts.extend(
                [
                    f"Missing item results: {', '.join(missing)}.",
                    "",
                ]
            )
        for track in TRACKS:
            track_rows = [results[i] for i in track["ids"] if i in results]
            if not track_rows:
                continue
            parts.extend(
                [
                    f"## {track['title']}",
                    "",
                    track["blurb"],
                    "",
                    summary_table(attach_models(summarize(track_rows), RESULT_DIRS)),
                    "",
                ]
            )
        sample_parts = []
        for item_id, label in SAMPLES:
            if item_id in results:
                sample_parts.append(
                    sample_block(item_id, label, dataset, results[item_id])
                )
        if sample_parts:
            parts.extend(
                [
                    "## Examples",
                    "",
                    "Each sample shows the raw source or the task, the baseline rewrite,",
                    "and the skill-based rewrite. Long texts are cut after about 900",
                    "characters.",
                    "",
                    "\n\n".join(sample_parts),
                    "",
                ]
            )
    else:
        parts.extend(
            [
                "## Latest results",
                "",
                "No item outputs yet. Run the commands in How to run, then",
                "`uv run python evals/write_readme.py`.",
                "",
            ]
        )

    README.write_text("\n".join(parts).rstrip() + "\n")
    print(f"Wrote {README} from {len(results)} item results")


if __name__ == "__main__":
    main()
