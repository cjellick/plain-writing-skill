#!/usr/bin/env python3
"""Sample long Claude Fable 5 coding traces into fable_histories/.

Each item keeps the full coding-agent trace. The eval asks a model to rewrite
the longest assistant wrap-up in that trace, not necessarily the last message.
"""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path

from datasets import load_dataset

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "sources" / "fable_histories"
DATASET = ROOT / "dataset.jsonl"
SOURCE_NAME = "greghavens/fable-5-coding-and-debugging-traces"
N_TRACES = 15
MIN_WRAPUP_CHARS = 2800
MIN_MESSAGES = 28
SKIP_CATEGORIES = {"seed-authoring"}
LANG_CAP = 4
FAMILY_CAP = 8

FABLE_REWRITE_PROMPT = (
    "The coding-agent history above includes a long wrap-up written in a "
    "fable-style voice. Rewrite the wrap-up below so a sharp technical reader "
    "with no project context can understand it. Follow the plain-writing "
    "guidelines. Keep the concrete facts from that wrap-up and the rest of "
    "the trace. Do not invent work that is not in the history. Return only "
    "the rewrite.\n\nWrap-up:\n{wrapup}"
)

LANG_ALIASES = {
    "py": "python",
    "ts": "typescript",
    "js": "javascript",
    "English": "en",
}


def category_family(category: str) -> str:
    if category.startswith("full-distill"):
        return "full-distill"
    if category.startswith("project-"):
        return "project"
    if category.startswith("feature-"):
        return "feature"
    if category.startswith("debug") or category.startswith("compilefix"):
        return "debug"
    if category.startswith("build-"):
        return "build"
    return category


def norm_lang(lang: str) -> str:
    return LANG_ALIASES.get(lang, lang)


def is_wrapup_message(message: dict) -> bool:
    if message.get("role") != "assistant":
        return False
    if message.get("tool_calls"):
        return False
    return bool((message.get("content") or "").strip())


def longest_wrapup(messages: list[dict]) -> tuple[int, str]:
    best_i = -1
    best_text = ""
    for i, message in enumerate(messages):
        if not is_wrapup_message(message):
            continue
        text = (message.get("content") or "").strip()
        if len(text) > len(best_text):
            best_i = i
            best_text = text
    return best_i, best_text


def longest_cleaned_wrapup(messages: list[dict]) -> tuple[int, str]:
    best_i = -1
    best_text = ""
    for i, message in enumerate(messages):
        if message.get("role") != "assistant":
            continue
        text = (message.get("content") or "").strip()
        if not text or "[tool_call " in text:
            continue
        if len(text) > len(best_text):
            best_i = i
            best_text = text
    return best_i, best_text


def message_to_text(message: dict) -> str:
    chunks: list[str] = []
    content = message.get("content") or ""
    if content.strip():
        chunks.append(content.strip())
    for call in message.get("tool_calls") or []:
        fn = call.get("function") or {}
        name = fn.get("name") or call.get("name") or "unknown"
        args = fn.get("arguments") or ""
        if not isinstance(args, str):
            args = json.dumps(args, ensure_ascii=False)
        chunks.append(f"[tool_call {name}] {args}")
    return "\n".join(chunks).strip()


def raw_messages_to_chat(raw_messages: list) -> list[dict]:
    cleaned: list[dict] = []
    for message in raw_messages:
        role = message.get("role")
        if role not in ("user", "assistant", "system", "tool"):
            continue
        content = message_to_text(message)
        if role == "tool":
            role = "user"
            name = message.get("name") or ""
            prefix = f"[tool_result {name}]\n" if name else "[tool_result]\n"
            content = prefix + content if content else prefix.rstrip()
        elif role == "system":
            role = "user"
            content = f"[system]\n{content}" if content else ""
        if not content:
            continue
        if cleaned and cleaned[-1]["role"] == role:
            cleaned[-1]["content"] += "\n\n" + content
        else:
            cleaned.append({"role": role, "content": content})
    return cleaned


def pick_rows(complete: list[dict]) -> list[dict]:
    candidates: list[dict] = []
    for row in complete:
        if row["category"] in SKIP_CATEGORIES:
            continue
        _, wrapup = longest_wrapup(row["messages"])
        if len(wrapup) < MIN_WRAPUP_CHARS:
            continue
        if row["n_messages"] < MIN_MESSAGES:
            continue
        item = dict(row)
        item["_wrapup"] = wrapup
        item["_wrapup_len"] = len(wrapup)
        candidates.append(item)
    candidates.sort(
        key=lambda r: (-r["_wrapup_len"], -r["n_messages"], -r["assistant_steps"])
    )

    picked: list[dict] = []
    lang_counts: Counter[str] = Counter()
    family_counts: Counter[str] = Counter()
    seen_tasks: set[str] = set()
    for row in candidates:
        task = row["task"]
        if task in seen_tasks:
            continue
        lang = norm_lang(row["lang"])
        family = category_family(row["category"])
        if lang_counts[lang] >= LANG_CAP:
            continue
        if family_counts[family] >= FAMILY_CAP:
            continue
        picked.append(row)
        seen_tasks.add(task)
        lang_counts[lang] += 1
        family_counts[family] += 1
        if len(picked) >= N_TRACES:
            break
    if len(picked) < N_TRACES:
        for row in candidates:
            if row["task"] in seen_tasks:
                continue
            picked.append(row)
            seen_tasks.add(row["task"])
            if len(picked) >= N_TRACES:
                break
    if len(picked) < N_TRACES:
        raise SystemExit(f"Expected {N_TRACES} fable traces, got {len(picked)}")
    picked.sort(key=lambda r: (-r["_wrapup_len"], -r["n_messages"], -r["assistant_steps"]))
    return picked


def rewrite_dataset(new_items: list[dict]) -> None:
    kept: list[dict] = []
    with DATASET.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            if item.get("category") == "fable_coding":
                continue
            kept.append(item)
    kept.extend(new_items)
    kept.sort(key=lambda item: int(item["id"]))
    DATASET.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in kept))
    print(f"Wrote {len(kept)} items to {DATASET}")


def main() -> None:
    print(f"Loading {SOURCE_NAME}...")
    ds = load_dataset(SOURCE_NAME, split="train")
    complete = [row for row in ds if row["assistant_step"] == row["assistant_steps"]]
    selected = pick_rows(complete)

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    new_items: list[dict] = []
    for i, row in enumerate(selected, start=1):
        messages = raw_messages_to_chat(row["messages"])
        wrap_i, wrapup = longest_cleaned_wrapup(messages)
        if wrap_i < 0 or not wrapup:
            raise SystemExit(f"{row['task']} has no assistant wrap-up")
        hist_name = f"history_{i:02d}.json"
        payload = {
            "source_dataset": SOURCE_NAME,
            "task": row["task"],
            "source_trajectory_id": row.get("source_trajectory_id") or row["task"],
            "lang": row["lang"],
            "trace_category": row["category"],
            "teacher_model": row.get("teacher_model") or "anthropic/claude-fable-5",
            "observed_models": list(row.get("observed_models") or []),
            "assistant_steps": row["assistant_steps"],
            "n_messages_source": row["n_messages"],
            "wrapup_index": wrap_i,
            "wrapup_chars": len(wrapup),
            "message_count": len(messages),
            "messages": messages,
        }
        (OUT_DIR / hist_name).write_text(json.dumps(payload, ensure_ascii=False) + "\n")
        chars = sum(len(m["content"]) for m in messages)
        print(
            f"{hist_name}: {row['task']} {row['category']} {row['lang']} "
            f"nmsg={row['n_messages']} wrapup={len(wrapup)}@{wrap_i} chars={chars}"
        )
        new_items.append(
            {
                "id": f"{50 + i:02d}",
                "category": "fable_coding",
                "source_kind": "fable_coding_trajectory",
                "source": {
                    "dataset": SOURCE_NAME,
                    "task": row["task"],
                    "lang": row["lang"],
                    "trace_category": row["category"],
                    "teacher_model": payload["teacher_model"],
                    "assistant_steps": row["assistant_steps"],
                    "n_messages": row["n_messages"],
                    "wrapup_chars": len(wrapup),
                    "wrapup_index": wrap_i,
                },
                "history_file": f"fable_histories/{hist_name}",
                "prompt": FABLE_REWRITE_PROMPT.format(wrapup=wrapup),
            }
        )

    rewrite_dataset(new_items)


if __name__ == "__main__":
    main()
