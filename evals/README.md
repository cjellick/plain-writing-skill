# Plain-writing evals

These evals ask whether giving `SKILL.md` to a writer produces text that
follows the plain-writing rules better than a writer that does not see
the skill.

## Eval procedure

### Dataset

`dataset.jsonl` has 67 writing tasks.

- `01`–`40`: short prompts, public-domain excerpts, and LLM slop.
- `41`–`50`: long research and support-agent histories.
- `51`–`65`: Claude Fable 5 coding-agent traces. The writer sees the
  full trace and is asked to rewrite the longest wrap-up.
- `66`–`67`: chat context and short-list checks.

For a history task, we load a conversation from `sources/` and append
the prompt as the last user turn. Fable traces are rebuilt with
`uv run python build_fable_histories.py`.

### Baseline

The same user messages are sent to the writer with a short system prompt:
write a clear, complete response, and return only the requested writing.
The writer does not see `SKILL.md`.

### Skill condition

The same user messages are sent again, to the same model, with `SKILL.md`
in the system prompt. The writer is told to follow those rules. It does
not see the baseline output.

### How it is judged

For each writing task, we compare the two texts on every rule in
`SKILL.md`. The judge does not know which text used the skill. The skill
wins that task if it wins more rules. We also add up those rule wins
across tasks.

The default rewriter and judge are `gpt-5.5`. Override them with
`--model` and `--judge-model`.

## How to run

```
cd evals
uv sync
uv run python run_eval.py --out outputs/all
uv run python run_eval.py --category fable_coding --out outputs/fable_coding
uv run python run_eval.py --ids 66,67 --out outputs/new_rules
uv run python write_readme.py
```

Put `OPENAI_API_KEY` in a `.env` file at the repo root. Outputs land in
`outputs/` and are gitignored. `write_readme.py` combines the result
files from those folders and writes this README.

## Latest results

Combined from `67` of `67` writing tasks.

<table>
<thead>
<tr>
<th>Metric</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>Writing tasks</td>
<td>67</td>
</tr>
<tr>
<td>Skill / baseline / tie</td>
<td>65 / 2 / 0</td>
</tr>
<tr>
<td>Win rate among decisive tasks</td>
<td>97%</td>
</tr>
<tr>
<td>Rule skill / baseline / tie</td>
<td>705 / 232 / 738</td>
</tr>
<tr>
<td>Rule win rate among decisive</td>
<td>75%</td>
</tr>
<tr>
<td>Errors</td>
<td>0</td>
</tr>
<tr>
<td>Rewriter / judge</td>
<td>gpt-5.5 / gpt-5.5</td>
</tr>
</tbody>
</table>

### Rules with the largest gap

<table>
<thead>
<tr>
<th>Rule</th>
<th>Skill / baseline / tie</th>
</tr>
</thead>
<tbody>
<tr>
<td>1. Use simple, everyday words.</td>
<td>61 / 5 / 1 (92%)</td>
</tr>
<tr>
<td>2. No jargon.</td>
<td>52 / 4 / 11 (93%)</td>
</tr>
<tr>
<td>15. No dashes or middle dots.</td>
<td>35 / 1 / 31 (97%)</td>
</tr>
<tr>
<td>8. Write complete sentences.</td>
<td>40 / 7 / 20 (85%)</td>
</tr>
<tr>
<td>10. Organize a paragraph as a topic sentence and then support.</td>
<td>45 / 13 / 9 (78%)</td>
</tr>
<tr>
<td>17. Use straight quotes, not curly quotes.</td>
<td>33 / 1 / 33 (97%)</td>
</tr>
<tr>
<td>3. No puffery or empty emphasis.</td>
<td>27 / 2 / 38 (93%)</td>
</tr>
<tr>
<td>6. Do not invent hyphenated adjectives.</td>
<td>27 / 2 / 38 (93%)</td>
</tr>
</tbody>
</table>

Rules where the baseline won more often:

<table>
<thead>
<tr>
<th>Rule</th>
<th>Skill / baseline / tie</th>
</tr>
</thead>
<tbody>
<tr>
<td>5. It's ok to use contractions.</td>
<td>8 / 9 / 50 (47%)</td>
</tr>
<tr>
<td>11. Never write three or more clauses in one sentence, or three or more example sentences in a row.</td>
<td>22 / 38 / 7 (37%)</td>
</tr>
</tbody>
</table>

## Examples

Some tasks rewrite existing text. Some tasks write from scratch.
The first column is original writing for a rewrite, and the prompt
for a write-from-scratch task. Long texts are cut after about
320 characters.

### Rewrite tasks

These start from existing text. The first column is that original writing.

<table>
<thead>
<tr>
<th>Original writing</th>
<th>Baseline (no skill)</th>
<th>Skill-based</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="3">
<strong>Product launch copy</strong>, task 05, 
<code>docs_skill</code>, 
judge 17-2-6
</td>
</tr>
<tr>
<td valign="top">**Introducing CodeClarify™: The Plain-Writing Revolution for Your AI Agents**<br><br>We're not just teaching agents to code—we're teaching them to *communicate*.<br><br>Meet **Semantic Simplicity Engine**, the breakthrough capability that transforms your coding agents from technical translators into plain-language virtuosos. Becau<br><br>[...]</td>
<td valign="top">**Introducing CodeClarify™: Plain Writing for AI Coding Agents**<br><br>CodeClarify helps AI coding agents explain code clearly, not just write it.<br><br>The **Semantic Simplicity Engine** is a capability that converts technical explanations into plain language. It helps agents describe complex code, logic, and design decisions i<br><br>[...]</td>
<td valign="top">CodeClarify is a plain writing feature for AI coding agents. It helps agents explain code and technical decisions in clear, everyday language.<br><br>AI coding agents can write working functions, but their explanations can be hard to understand. CodeClarify addresses that problem by making the agent explain what the code doe<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Slide script</strong>, task 08, 
<code>slides_script</code>, 
judge 17-2-6
</td>
</tr>
<tr>
<td valign="top"># Crushing Eval Costs: The Sampling Revolution<br><br>**The Problem Space**<br>Full dataset evaluation. Expensive. Prohibitive. Your burn rate? Astronomical. Every benchmark run: hundreds of dollars. Thousands. Enterprise scale? Forget it.<br><br>**Enter: Strategic Sampling**<br>We're not testing every grain of sand to understand the be<br><br>[...]</td>
<td valign="top"># Reducing Evaluation Costs with Strategic Sampling<br><br>## Problem<br><br>Running evaluations on a full dataset can be expensive. A single benchmark run may cost hundreds or thousands of dollars, and at enterprise scale the cost can become prohibitive. This limits how often teams can evaluate models, run experiments, or perform<br><br>[...]</td>
<td valign="top"># Reduce evaluation costs with sampling<br><br>Full dataset evaluation can be expensive. A benchmark run can cost hundreds or thousands of dollars, and the cost can block frequent evaluation at enterprise scale.<br><br>Sampling reduces evaluation cost by running the evaluation on a representative subset of the dataset instead of t<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Product memo</strong>, task 02, 
<code>eval_harness</code>, 
judge 21-2-2
</td>
</tr>
<tr>
<td valign="top">**PRODUCT MEMO: PROMETHEAN EVAL HARNESS**<br><br>**RE: Operationalizing PM Intuition Through Systematic LLM Validation**<br><br>We're at an inflection point. Product teams ship features. Engineering teams ship code. But who validates the *intelligence layer*? <br><br>Enter **Promethean**: the first eval harness purpose-built for Product<br><br>[...]</td>
<td valign="top">**Product Memo: Promethean Eval Harness**<br><br>**Subject: A validation tool for product managers building with LLMs**<br><br>Product teams ship features. Engineering teams ship code. But LLM-based products also need a reliable way to validate model behavior: output quality, safety, reasoning, latency, tone, and fit for the inten<br><br>[...]</td>
<td valign="top"># Product memo: Promethean eval harness<br><br>Product teams need a consistent way to evaluate LLM outputs before they ship features that depend on them.<br><br>Product managers often compare model outputs in Slack threads or by personal judgment. For example, they may need to decide whether GPT 4 is better than Claude for a speci<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Fable wrap-up</strong>, task 57, 
<code>powershell-meraki-link-pages</code>, 
judge 13-5-7
</td>
</tr>
<tr>
<td valign="top">Done. `pwsh -NoProfile -File test_meraki_pages.ps1` exits 0 with all 50 checks passing, and every rejection finding from the prior review is fixed and verified by adversarial loopback probes (probe scripts were scratch and have been removed). Protected files (`test_meraki_pages.ps1`, `docs/`) are untouched — git status<br><br>[...]</td>
<td valign="top">Implemented and verified the Meraki Dashboard API v1 PowerShell module.<br><br>`pwsh -NoProfile -File test_meraki_pages.ps1` passes with `OK (50 checks)`. I also ran separate loopback probes for the prior review issues; those passed, and the scratch probe file was removed. Protected files were not changed: `test_meraki_pages<br><br>[...]</td>
<td valign="top">The Meraki PowerShell module is implemented, and the acceptance test passes. I ran `pwsh -NoProfile -File test_meraki_pages.ps1`, and it exited 0 with all 50 checks passing. I did not edit the protected files, including `test_meraki_pages.ps1` and everything under `docs/`. The only new files are the four module files.<br><br>[...]</td>
</tr>
</tbody>
</table>

### Write-from-scratch tasks

These start from a prompt. There is no original writing, so the first
column is the prompt.

<table>
<thead>
<tr>
<th>Prompt</th>
<th>Baseline (no skill)</th>
<th>Skill-based</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="3">
<strong>Slide titles</strong>, task 25, 
<code>slides</code>, 
judge 17-3-5
</td>
</tr>
<tr>
<td valign="top">Write 5 slide titles and one short supporting sentence each for a talk about reducing LLM eval cost with sampling.</td>
<td valign="top">1. **Why LLM Eval Costs Add Up Fast**  <br>   Large test sets, repeated model runs, and human or model-graded judgments can make evaluation expensive at scale.<br><br>2. **Sampling Preserves Signal While Cutting Spend**  <br>   Evaluating a representative subset can reveal performance trends without running every example every tim<br><br>[...]</td>
<td valign="top">1. Measure less, but keep the signal  <br>Sampling lets you score a smaller set of examples while still estimating whether model quality changed.<br><br>2. Start with the decision you need to make  <br>Choose the sample size based on the change you need to detect, not on the full size of the test set.<br><br>3. Use random sampling to av<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Support reply</strong>, task 32, 
<code>faq_support</code>, 
judge 12-3-10
</td>
</tr>
<tr>
<td valign="top">Answer this user question helpfully:<br>Why did my export fail with "schema mismatch" after yesterday's deploy?</td>
<td valign="top">Your export likely failed because yesterday’s deploy changed the data schema that the export job expects.<br><br>A “schema mismatch” usually means the exporter expected one set of fields, types, or column names, but the data now has something different. Common causes include:<br><br>- A column was renamed, removed, or added<br>- A fi<br><br>[...]</td>
<td valign="top">Your export likely failed because yesterday's deploy changed the shape of the data that the exporter writes, but the export schema was not updated at the same time.<br><br>A "schema mismatch" means the exporter produced data with fields or types that did not match what the destination expected. For example, the deploy may ha<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Engineering brief</strong>, task 67, 
<code>project_update</code>, 
judge 11-3-11
</td>
</tr>
<tr>
<td valign="top">Write a short Slack brief for engineering. Cover these facts: search ranking moved from heuristics to a scored model, p95 latency went from 900ms to 220ms, recall on long queries is still untested, the old heuristic path is still in the repo as a fallback, dark mode shipped, the invite link bug is fixed, analytics expo<br><br>[...]</td>
<td valign="top">Engineering brief:<br><br>- Search ranking has moved from heuristics to a scored model.<br>- Search p95 latency improved from ~900ms to ~220ms.<br>- Recall on long queries is still untested and needs validation.<br>- The old heuristic ranking path remains in the repo as a fallback.<br>- Dark mode has shipped.<br>- The invite link bug is fi<br><br>[...]</td>
<td valign="top">Search ranking now uses a scored model instead of heuristics, and p95 latency fell from 900 ms to 220 ms. The old heuristic path is still in the repo as a fallback. To do: test recall on long queries.<br><br>Shipped:<br>- Dark mode<br>- Invite link fix<br>- Renderer cleanup<br>- Small copy edits<br><br>Blocked:<br>- Analytics export is blocked o<br><br>[...]</td>
</tr>
</tbody>
</table>
