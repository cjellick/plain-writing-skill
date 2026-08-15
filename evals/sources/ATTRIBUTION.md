# Source attribution for eval texts

## Public-domain excerpts

Excerpts in `clear_excerpts.json` come from the [CLEAR Corpus](https://github.com/scrosseye/CLEAR-Corpus).
We selected Project Gutenberg excerpts whose CLEAR `License` field is empty, which the CLEAR documentation treats as public-domain passages.

CLEAR Corpus citation: Crossley, S. A., et al. CommonLit Ease of Readability (CLEAR) Corpus.

Each excerpt record keeps the original title, author, Gutenberg URL, and CLEAR id.

## LLM-generated slop

Texts in `llm_slop.json` were generated with Anthropic Claude for the deslopify track.
They are synthetic AI-sounding drafts created for evaluation, not copied from third-party pages.

## Agentic research and support histories

Files under `agent_histories/` are truncated conversation histories sampled from
[DiscoPosse/agent-llm-traces](https://huggingface.co/datasets/DiscoPosse/agent-llm-traces)
(collected around May–June 2026).

We keep the longest Claude Opus 4.5 traces from:

- `browsecompplus` (deep research / web browsing)
- `tau2_*` (airline, retail, telecom customer-support agents)

Each history file records `source_dataset`, `benchmark`, `session_id`, and
`models`. Histories are rebuilt from the final OpenTelemetry span’s
`gen_ai.input.messages` and truncated to about 180k characters for cost.

Downstream use follows the upstream dataset card and any model-provider usage
policies noted there.

## Fable coding-agent histories

Files under `fable_histories/` are complete coding-agent conversations sampled
from
[greghavens/fable-5-coding-and-debugging-traces](https://huggingface.co/datasets/greghavens/fable-5-coding-and-debugging-traces).

The upstream rows are cumulative prefixes of Claude Fable 5 (`anthropic/claude-fable-5`)
sessions. We keep the final prefix of each selected task (the full trace)
and skip seed-authoring rows. Selection prefers the longest assistant wrap-up,
then caps repeats by language and task family.

Each history file records `source_dataset`, `task`, `lang`, `trace_category`,
and `teacher_model`. The stored conversation keeps the full tool calls and
tool results from the selected trace. Consecutive same-role turns are merged
only so the chat writer can send them.

The eval prompt asks a model to rewrite the longest wrap-up in plain writing,
with the rest of the trace available as context.

Downstream use follows the upstream dataset card and any model-provider usage
policies noted there.
