#!/usr/bin/env python3
"""Sample longest DiscoPosse BrowseComp/TAU Opus traces into agent_histories/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from datasets import load_dataset

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "sources" / "agent_histories"
DATASET = ROOT / "dataset.jsonl"
MAX_CHARS = 180_000
N_BROWSE = 7
N_TAU = 3


def parts_to_text(parts: list | None) -> str:
    chunks: list[str] = []
    for part in parts or []:
        ptype = part.get("type")
        if ptype == "text":
            chunks.append(part.get("content") or part.get("text") or "")
        elif ptype == "tool_call":
            args = part.get("arguments")
            chunks.append(
                f"[tool_call {part.get('name')}] "
                f"{json.dumps(args, ensure_ascii=False)[:3000]}"
            )
        elif ptype == "tool_call_response":
            result = part.get("result")
            if isinstance(result, list):
                texts = []
                for item in result:
                    if isinstance(item, dict):
                        texts.append(str(item.get("text") or item.get("content") or item)[:4000])
                    else:
                        texts.append(str(item)[:4000])
                chunks.append("[tool_result]\n" + "\n".join(texts))
            else:
                chunks.append(f"[tool_result]\n{str(result)[:6000]}")
        else:
            chunks.append(f"[{ptype}] {json.dumps(part, ensure_ascii=False)[:2000]}")
    return "\n".join(c for c in chunks if c).strip()


def otel_messages_to_chat(raw_messages: list) -> list[dict]:
    cleaned: list[dict] = []
    for message in raw_messages:
        role = message.get("role")
        if role not in ("user", "assistant", "system", "tool"):
            continue
        content = parts_to_text(message.get("parts"))
        if not content:
            continue
        # Map system/tool into user/assistant for the OpenAI chat writer path.
        if role == "system":
            role = "user"
        elif role == "tool":
            role = "user"
            content = f"[tool]\n{content}"
        if cleaned and cleaned[-1]["role"] == role:
            cleaned[-1]["content"] += "\n\n" + content
        else:
            cleaned.append({"role": role, "content": content})
    return cleaned


def truncate_messages(messages: list[dict], max_chars: int) -> list[dict]:
    total = sum(len(m["content"]) for m in messages)
    if total <= max_chars:
        return messages
    # Keep the first message (task setup) and as many recent turns as fit.
    if not messages:
        return messages
    head = messages[0]
    budget = max_chars - len(head["content"]) - 80
    tail: list[dict] = []
    for message in reversed(messages[1:]):
        n = len(message["content"]) + 2
        if n > budget:
            break
        tail.append(message)
        budget -= n
    tail.reverse()
    marker = {
        "role": "user",
        "content": "[earlier turns omitted for length]",
    }
    return [head, marker, *tail]


def model_is_opus(models: list) -> bool:
    return any("opus" in str(m).lower() for m in (models or []))


def last_span_fingerprint(spans: list) -> str:
    if not spans:
        return ""
    attrs = spans[-1].get("attributes") or {}
    raw = attrs.get("gen_ai.input.messages") or ""
    if not isinstance(raw, str):
        raw = json.dumps(raw, ensure_ascii=False)
    # Cheap content fingerprint without hashing the full multi-MB blob twice.
    return f"{len(raw)}:{raw[:200]}:{raw[-200:]}"


def pick_unique(rows: list[dict], n: int) -> list[dict]:
    picked: list[dict] = []
    seen: set[str] = set()
    for row in rows:
        fp = last_span_fingerprint(row["spans"])
        if fp in seen:
            continue
        seen.add(fp)
        picked.append(row)
        if len(picked) >= n:
            break
    return picked


def pick_rows(ds) -> list[dict]:
    browse: list[dict] = []
    tau: list[dict] = []
    for idx, row in enumerate(ds):
        if not model_is_opus(row["models"]):
            continue
        bench = row["benchmark"]
        item = {
            "dataset_index": idx,
            "benchmark": bench,
            "models": [str(m) for m in (row["models"] or [])],
            "session_id": row["session_id"],
            "max_tokens": row["max_tokens"],
            "total_tokens": row["total_tokens"],
            "n_spans": len(row["spans"] or []),
            "spans": row["spans"],
            "collected_at": row["collected_at"],
        }
        if bench == "browsecompplus":
            browse.append(item)
        elif str(bench).startswith("tau2"):
            tau.append(item)
    browse.sort(key=lambda r: (-r["max_tokens"], -r["total_tokens"]))
    # Prefer domain diversity among the longest TAU traces.
    tau.sort(key=lambda r: (-r["max_tokens"], -r["total_tokens"]))
    tau_by_domain: list[dict] = []
    leftovers: list[dict] = []
    seen_domains: set[str] = set()
    for row in tau:
        if row["benchmark"] not in seen_domains:
            seen_domains.add(row["benchmark"])
            tau_by_domain.append(row)
        else:
            leftovers.append(row)
    tau_ordered = tau_by_domain + leftovers
    return pick_unique(browse, N_BROWSE) + pick_unique(tau_ordered, N_TAU)


def history_prompt(benchmark: str) -> str:
    if benchmark == "browsecompplus":
        return (
            "Using only the research-agent history above, write a plain status note "
            "for a technical reader with no prior context. Cover: the question being "
            "researched, the main search path, the best current answer if any, and "
            "what is still uncertain. Keep concrete facts. Return only the note."
        )
    return (
        "Using only the customer-support agent history above, write a plain handoff "
        "note for the next agent. Cover: customer goal, steps already taken, tools "
        "or policy checks already used, current state, and the next action. Keep "
        "concrete facts. Return only the note."
    )


def main() -> None:
    print("Loading DiscoPosse/agent-llm-traces...")
    ds = load_dataset("DiscoPosse/agent-llm-traces", split="train")
    selected = pick_rows(ds)
    if len(selected) < N_BROWSE + N_TAU:
        raise SystemExit(f"Expected {N_BROWSE + N_TAU} rows, got {len(selected)}")

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    long_items: list[dict] = []
    for i, row in enumerate(selected, start=1):
        spans = row["spans"] or []
        last = spans[-1]
        attrs = last.get("attributes") or {}
        raw = attrs.get("gen_ai.input.messages")
        if isinstance(raw, str):
            otel_messages = json.loads(raw)
        else:
            otel_messages = raw or []
        messages = truncate_messages(otel_messages_to_chat(otel_messages), MAX_CHARS)
        hist_name = f"history_{i:02d}.json"
        payload = {
            "source_dataset": "DiscoPosse/agent-llm-traces",
            "benchmark": row["benchmark"],
            "session_id": row["session_id"],
            "dataset_index": row["dataset_index"],
            "models": row["models"],
            "max_tokens": row["max_tokens"],
            "total_tokens": row["total_tokens"],
            "n_spans": row["n_spans"],
            "collected_at": row["collected_at"],
            "truncated_to_chars": MAX_CHARS,
            "message_count": len(messages),
            "messages": messages,
        }
        (OUT_DIR / hist_name).write_text(json.dumps(payload, ensure_ascii=False) + "\n")
        chars = sum(len(m["content"]) for m in messages)
        print(
            f"{hist_name}: {row['benchmark']} max_tok={row['max_tokens']} "
            f"msgs={len(messages)} chars={chars} session={row['session_id']}"
        )
        long_items.append(
            {
                "id": f"{40 + i:02d}",
                "category": "long_history",
                "source_kind": "agent_trajectory",
                "source": {
                    "dataset": "DiscoPosse/agent-llm-traces",
                    "benchmark": row["benchmark"],
                    "session_id": row["session_id"],
                    "models": row["models"],
                    "max_tokens": row["max_tokens"],
                },
                "history_file": f"agent_histories/{hist_name}",
                "prompt": history_prompt(row["benchmark"]),
            }
        )

    # Rewrite dataset.jsonl: keep items 01-40, replace 41-50.
    kept: list[dict] = []
    with DATASET.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            if int(item["id"]) <= 40:
                kept.append(item)
    kept.extend(long_items)
    DATASET.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in kept))
    print(f"Wrote {len(kept)} items to {DATASET}")


if __name__ == "__main__":
    main()
