#!/usr/bin/env python3
"""Run a small before/after eval of the plain-writing skill.

Usage:
  uv sync
  uv run python evals/run_eval.py
  uv run python evals/run_eval.py --limit 5
  uv run python evals/run_eval.py --category long_history --limit 1
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
EVALS = Path(__file__).resolve().parent
SOURCES = EVALS / "sources"
DATASET = EVALS / "dataset.jsonl"
SKILL = ROOT / "SKILL.md"
DEFAULT_OUT = EVALS / "outputs"

BASELINE_SYSTEM = (
    "You are a helpful writing assistant. Write a clear, complete response. "
    "Return only the requested writing."
)

JUDGE_SYSTEM = """You judge which of two texts better follows a plain-writing skill.

Score only against the skill rules. Prefer the text that is plainer, more literal,
less hype-driven, and still complete. If both are similar, pick the one with fewer
rule breaks. If one drops important facts, prefer the more complete one.

Return ONLY valid JSON with these keys:
- winner: "a", "b", or "tie"
- skill_better: true if the skill condition won, false if baseline won, null if tie
- baseline_violations: array of short rule-break labels in text A
- skill_violations: array of short rule-break labels in text B
- reason: one or two sentences
"""


def load_dataset(
    path: Path,
    limit: int | None = None,
    category: str | None = None,
    ids: set[str] | None = None,
) -> list[dict]:
    items = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            if category and item.get("category") != category:
                continue
            if ids and item.get("id") not in ids:
                continue
            items.append(item)
            if limit is not None and len(items) >= limit:
                break
    return items


def load_history_messages(item: dict) -> list[dict]:
    history_file = item.get("history_file")
    if not history_file:
        return []
    path = SOURCES / history_file
    payload = json.loads(path.read_text())
    messages = payload.get("messages") or []
    cleaned = []
    for message in messages:
        role = message.get("role")
        content = message.get("content", "")
        if role not in ("user", "assistant"):
            continue
        if not isinstance(content, str) or not content.strip():
            continue
        cleaned.append({"role": role, "content": content})
    return cleaned


def build_messages(item: dict) -> list[dict]:
    history = load_history_messages(item)
    prompt = item["prompt"]
    if not history:
        return [{"role": "user", "content": prompt}]
    messages = list(history)
    if messages and messages[-1]["role"] == "user":
        messages[-1]["content"] += "\n\n" + prompt
    else:
        messages.append({"role": "user", "content": prompt})
    return messages


def complete(
    client: Anthropic,
    model: str,
    system: str,
    messages: list[dict],
    max_tokens: int = 1200,
) -> str:
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    parts = []
    for block in message.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "".join(parts).strip()


def judge_pair(
    client: Anthropic,
    model: str,
    skill_text: str,
    prompt: str,
    baseline: str,
    with_skill: str,
) -> dict:
    user = f"""Skill rules:

{skill_text}

Task prompt:
{prompt}

Text A (baseline, no skill):
{baseline}

Text B (with skill):
{with_skill}
"""
    raw = complete(
        client,
        model,
        JUDGE_SYSTEM,
        [{"role": "user", "content": user}],
        max_tokens=800,
    )
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:].strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "winner": "tie",
            "skill_better": None,
            "baseline_violations": [],
            "skill_violations": [],
            "reason": f"Judge returned non-JSON: {raw[:300]}",
        }
    winner = result.get("winner")
    if winner == "b":
        result["skill_better"] = True
    elif winner == "a":
        result["skill_better"] = False
    elif winner == "tie":
        result["skill_better"] = None
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None, help="Run only the first N matching items")
    parser.add_argument("--category", default=None, help="Only run this category")
    parser.add_argument(
        "--ids",
        default=None,
        help="Comma-separated item ids to run, e.g. 41,42",
    )
    parser.add_argument("--model", default="claude-sonnet-4-5-20250929")
    parser.add_argument(
        "--judge-model",
        default="claude-haiku-4-5-20251001",
        help="Judge model (defaults to Haiku for cost)",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--sleep", type=float, default=0.2, help="Pause between API calls")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY is missing. Put it in .env at the repo root.", file=sys.stderr)
        return 1

    skill_text = SKILL.read_text()
    ids = {part.strip() for part in args.ids.split(",")} if args.ids else None
    items = load_dataset(DATASET, args.limit, args.category, ids)
    if not items:
        print(f"No items found in {DATASET}", file=sys.stderr)
        return 1

    client = Anthropic(api_key=api_key)
    judge_model = args.judge_model
    args.out.mkdir(parents=True, exist_ok=True)

    results = []
    wins = ties = losses = 0

    skill_system = (
        "Follow the plain-writing skill below exactly when you write.\n\n"
        f"{skill_text}\n\n"
        "Return only the requested writing."
    )

    for i, item in enumerate(items, start=1):
        item_id = item["id"]
        prompt = item["prompt"]
        category = item.get("category", "")
        messages = build_messages(item)
        history_chars = sum(len(m["content"]) for m in messages[:-1]) if len(messages) > 1 else 0
        print(
            f"[{i}/{len(items)}] {item_id} ({category}) history_chars={history_chars}",
            flush=True,
        )

        max_tokens = 1600 if category == "long_history" else 1200
        baseline = complete(client, args.model, BASELINE_SYSTEM, messages, max_tokens)
        time.sleep(args.sleep)
        with_skill = complete(client, args.model, skill_system, messages, max_tokens)
        time.sleep(args.sleep)
        judgment = judge_pair(
            client, judge_model, skill_text, prompt, baseline, with_skill
        )
        time.sleep(args.sleep)

        skill_better = judgment.get("skill_better")
        if skill_better is True:
            wins += 1
        elif skill_better is False:
            losses += 1
        else:
            ties += 1

        row = {
            "id": item_id,
            "category": category,
            "prompt": prompt,
            "history_file": item.get("history_file"),
            "history_chars": history_chars,
            "baseline": baseline,
            "with_skill": with_skill,
            "judgment": judgment,
        }
        results.append(row)
        (args.out / f"{item_id}.json").write_text(json.dumps(row, indent=2) + "\n")

    summary = {
        "model": args.model,
        "judge_model": judge_model,
        "n": len(results),
        "skill_wins": wins,
        "baseline_wins": losses,
        "ties": ties,
        "skill_win_rate_among_decisive": (
            wins / (wins + losses) if (wins + losses) else None
        ),
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.out / "results.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in results)
    )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
