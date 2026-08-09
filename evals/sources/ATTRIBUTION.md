# Source attribution for eval texts

## Public-domain excerpts

Excerpts in `clear_excerpts.json` come from the [CLEAR Corpus](https://github.com/scrosseye/CLEAR-Corpus).
We selected Project Gutenberg excerpts whose CLEAR `License` field is empty, which the CLEAR documentation treats as public-domain passages.

CLEAR Corpus citation: Crossley, S. A., et al. CommonLit Ease of Readability (CLEAR) Corpus.

Each excerpt record keeps the original title, author, Gutenberg URL, and CLEAR id.

## LLM-generated slop

Texts in `llm_slop.json` were generated with Anthropic Claude for the deslopify track.
They are synthetic AI-sounding drafts created for evaluation, not copied from third-party pages.

## Agentic coding histories

Files under `agent_histories/` are truncated conversation histories sampled from
[thoughtworks/agentic-coding-trajectories](https://huggingface.co/datasets/thoughtworks/agentic-coding-trajectories).

That corpus is a derivative of upstream trajectory datasets. Each history file
records its `source_dataset` and `session_id`. Downstream use follows the
upstream dataset cards and any model-provider usage policies noted there:

- `nebius-swe-rebench-openhands`
- `swe-smith-claude-3-7-sonnet`
- `kwai-klear-swe-smith-mini`

Histories are truncated for cost and stored only to test whether plain-writing
instructions still hold after a long multi-turn coding-agent context.
