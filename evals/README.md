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
900 characters.

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
<code>docs_skill</code>. 
The skill won 17 rules, the baseline won 2, and 6 were ties.
</td>
</tr>
<tr>
<td valign="top">**Introducing CodeClarify™: The Plain-Writing Revolution for Your AI Agents**<br><br>We're not just teaching agents to code—we're teaching them to *communicate*.<br><br>Meet **Semantic Simplicity Engine**, the breakthrough capability that transforms your coding agents from technical translators into plain-language virtuosos. Because code that humans can't understand is code that can't scale.<br><br>**The Problem:** Your AI writes functions flawlessly but explains them like encrypted hieroglyphics.<br><br>**The Solution:** CodeClarify—where precision meets accessibility.<br><br>This isn't mere documentation. It's **contextual clarity engineering**. Our agents now deploy the Plain-Writing Protocol™, converting complex logic into digestible narratives that stakeholders, junior developers, and cross-functional teams actually comprehend. Think of it as a universal adapter for technical knowledge—bridging the gap between m<br><br>[...]</td>
<td valign="top">**Introducing CodeClarify™: Plain Writing for AI Coding Agents**<br><br>CodeClarify helps AI coding agents explain code clearly, not just write it.<br><br>The **Semantic Simplicity Engine** is a capability that converts technical explanations into plain language. It helps agents describe complex code, logic, and design decisions in a way that stakeholders, junior developers, and cross-functional teams can understand.<br><br>**The problem:** AI agents can write correct functions, but their explanations are often hard to follow.<br><br>**The solution:** CodeClarify makes technical communication more precise and accessible.<br><br>This goes beyond basic documentation. CodeClarify uses a **Plain-Writing Protocol™** to turn complex logic into clear explanations. It fills in missing context, avoids unnecessary jargon, and organizes information so readers can understand what the code does, why it works that way, and how to<br><br>[...]</td>
<td valign="top">CodeClarify is a plain writing feature for AI coding agents. It helps agents explain code and technical decisions in clear, everyday language.<br><br>AI coding agents can write working functions, but their explanations can be hard to understand. CodeClarify addresses that problem by making the agent explain what the code does, why it does it, and what assumptions the reader needs to know.<br><br>CodeClarify applies plain writing rules to agent output. The agent avoids unclear technical language when a simple word works, explains required technical terms, and spells out steps that might otherwise be treated as obvious. The agent also prefers active voice, so the explanation says who or what does each action.<br><br>The feature is meant to make technical writing easier to use for several groups, including stakeholders, junior developers, and teams outside engineering. For example, it can turn a complex impl<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Slide script</strong>, task 08, 
<code>slides_script</code>. 
The skill won 17 rules, the baseline won 2, and 6 were ties.
</td>
</tr>
<tr>
<td valign="top"># Crushing Eval Costs: The Sampling Revolution<br><br>**The Problem Space**<br>Full dataset evaluation. Expensive. Prohibitive. Your burn rate? Astronomical. Every benchmark run: hundreds of dollars. Thousands. Enterprise scale? Forget it.<br><br>**Enter: Strategic Sampling**<br>We're not testing every grain of sand to understand the beach. Smart sampling. Statistical rigor meets economic reality.<br><br>**The Math Checks Out**<br>95% confidence intervals. Representative subsets. 10% of data, 98% of insights. The magic of statistics working FOR you, not against you.<br><br>**Real-World Impact**<br>- 10x cost reduction, immediate<br>- Faster iteration cycles<br>- More experiments, same budget<br>- Hyperparameter sweeps suddenly affordable<br><br>**The Stratification Advantage**<br>Slice your data smartly. Category-aware sampling. Preserve distribution characteristics. Quality signals maintained. Performance metrics: stable.<br><br>**Confidence Wit<br><br>[...]</td>
<td valign="top"># Reducing Evaluation Costs with Strategic Sampling<br><br>## Problem<br><br>Running evaluations on a full dataset can be expensive. A single benchmark run may cost hundreds or thousands of dollars, and at enterprise scale the cost can become prohibitive. This limits how often teams can evaluate models, run experiments, or perform hyperparameter sweeps.<br><br>## Approach: Strategic Sampling<br><br>Instead of evaluating every example in the dataset, evaluate a statistically representative subset. The goal is to preserve the signal needed to make reliable decisions while reducing evaluation cost and runtime.<br><br>For example, evaluating 10% of the data may provide roughly 98% of the actionable insight, assuming the sample is representative and the evaluation is designed correctly.<br><br>## Statistical Basis<br><br>Sampling can provide reliable estimates when paired with statistical rigor:<br><br>- Use representative subsets of the f<br><br>[...]</td>
<td valign="top"># Reduce evaluation costs with sampling<br><br>Full dataset evaluation can be expensive. A benchmark run can cost hundreds or thousands of dollars, and the cost can block frequent evaluation at enterprise scale.<br><br>Sampling reduces evaluation cost by running the evaluation on a representative subset of the dataset instead of the full dataset. For example, you can evaluate 10 percent of the data and still capture about 98 percent of the signal, if the sample is representative and the error bounds are acceptable.<br><br>The statistical goal is to estimate the full dataset result with a known confidence level. For example, a 95 percent confidence interval gives a range that is likely to contain the true full dataset score. The margin of error shows how much uncertainty the sample adds.<br><br>Stratified sampling can make the estimate more reliable. With stratified sampling, you split the dataset by important c<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Product memo</strong>, task 02, 
<code>eval_harness</code>. 
The skill won 21 rules, the baseline won 2, and 2 were ties.
</td>
</tr>
<tr>
<td valign="top">**PRODUCT MEMO: PROMETHEAN EVAL HARNESS**<br><br>**RE: Operationalizing PM Intuition Through Systematic LLM Validation**<br><br>We're at an inflection point. Product teams ship features. Engineering teams ship code. But who validates the *intelligence layer*? <br><br>Enter **Promethean**: the first eval harness purpose-built for Product Managers navigating the LLM landscape. Think of it as your "CI/CD pipeline for prompt quality"—continuous validation that transforms vibes-based AI assessment into data-driven conviction.<br><br>Here's the unlock: PMs currently lack systematic frameworks to evaluate model outputs. Is GPT-4 actually better for your use case? Does Claude handle edge cases more gracefully? What about latency-quality tradeoffs? These questions live in Slack threads and gut feelings, creating a **validation gap** that blocks confident shipping.<br><br>Promethean introduces **Confidence Scaffolding™**—a thr<br><br>[...]</td>
<td valign="top">**Product Memo: Promethean Eval Harness**<br><br>**Subject: A validation tool for product managers building with LLMs**<br><br>Product teams ship features. Engineering teams ship code. But LLM-based products also need a reliable way to validate model behavior: output quality, safety, reasoning, latency, tone, and fit for the intended use case.<br><br>**Promethean** is an evaluation harness designed for Product Managers working with large language models. It provides a structured way to test prompts, compare models, and monitor output quality over time. In practice, it acts like a CI/CD pipeline for prompt and model quality: a repeatable validation process that replaces informal judgment with measurable evidence.<br><br>Today, PMs often do not have a systematic framework for evaluating LLM outputs. Questions such as these are usually answered through ad hoc reviews, Slack discussions, or intuition:<br><br>- Is GPT-4 b<br><br>[...]</td>
<td valign="top"># Product memo: Promethean eval harness<br><br>Product teams need a consistent way to evaluate LLM outputs before they ship features that depend on them.<br><br>Product managers often compare model outputs in Slack threads or by personal judgment. For example, they may need to decide whether GPT 4 is better than Claude for a specific use case, whether a model handles edge cases well, or whether a slower model gives better answers. Without a shared test process, teams have less confidence when they choose a model or change a prompt.<br><br>Promethean is an evaluation harness for product managers who work on LLM features. An evaluation harness is a tool that runs tests against model outputs and reports the results. Promethean helps product managers test prompt quality, model behavior, safety, domain accuracy, brand voice, tone, latency, and user preference.<br><br>Promethean has three evaluation layers:<br><br>1. Behav<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Fable wrap-up</strong>, task 58, 
<code>py-ontap-volume-job</code>. 
The skill won 12 rules, the baseline won 2, and 11 were ties.
</td>
</tr>
<tr>
<td valign="top">Done — `python3 test_ontap_volume.py` passes **52/52**, with only the new `ontapvol/` package added; `test_ontap_volume.py` and `docs/` are untouched.<br><br>## Contradictions between current official docs and the pinned contract (required report)<br><br>1. **Failed-job state name: `error` vs `failure`.** The current getting-started page states verbatim: *"If an operation fails for any reason, the job's `state` reports `error`"* — but `docs/contract.json` pins `failure` as the failed terminal state, and the endpoint-specific job reference supports the pinned value (*"After a job transitions to a failure or success state, it is deleted after a default time of 300 seconds"*). The two current official pages disagree with each other; the code treats **both** `failure` and `error` as the failed terminal state, so it satisfies the pinned contract and remains correct against either spelling. I did not edit<br><br>[...]</td>
<td valign="top">Implemented the stdlib-only `ontapvol` package. The acceptance command passes:<br><br>```text<br>python3 test_ontap_volume.py<br>passed=52 failed=0<br>```<br><br>Only the new `ontapvol/` package was added. `test_ontap_volume.py` and everything under `docs/` were left unchanged.<br><br>## Documentation mismatches found<br><br>1. **Failed job state: `error` vs `failure`**<br><br>   The current ONTAP REST getting-started documentation says:<br><br>   &gt; "If an operation fails for any reason, the job's `state` reports `error`"<br><br>   But `docs/contract.json` pins `failure` as the failed terminal state. The job endpoint reference also uses the pinned wording:<br><br>   &gt; "After a job transitions to a failure or success state, it is deleted after a default time of 300 seconds."<br><br>   The implementation treats both `failure` and `error` as failed terminal states. This satisfies the pinned contract and also handles the conflicting current documentatio<br><br>[...]</td>
<td valign="top">`python3 test_ontap_volume.py` passes with 52 checks passed and 0 failed. I added only the new `ontapvol/` package. I did not change `test_ontap_volume.py` or any file under `docs/`.<br><br>## Differences between current NetApp docs and the pinned contract<br><br>The current NetApp docs and the pinned contract disagree on one job state name. The current getting started page says: "If an operation fails for any reason, the job's `state` reports `error`". The pinned contract in `docs/contract.json` uses `failure` as the failed terminal state. The job endpoint reference also supports the pinned value with this text: "After a job transitions to a failure or success state, it is deleted after a default time of 300 seconds". The code treats both `failure` and `error` as failed terminal states, so it matches the pinned contract and also works with the wording from the getting started page.<br><br>The current Net<br><br>[...]</td>
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
<code>slides</code>. 
The skill won 17 rules, the baseline won 3, and 5 were ties.
</td>
</tr>
<tr>
<td valign="top">Write 5 slide titles and one short supporting sentence each for a talk about reducing LLM eval cost with sampling.</td>
<td valign="top">1. **Why LLM Eval Costs Add Up Fast**  <br>   Large test sets, repeated model runs, and human or model-graded judgments can make evaluation expensive at scale.<br><br>2. **Sampling Preserves Signal While Cutting Spend**  <br>   Evaluating a representative subset can reveal performance trends without running every example every time.<br><br>3. **Choose Samples That Match Your Risk**  <br>   Stratified, random, or targeted sampling helps focus evaluation effort on the cases that matter most.<br><br>4. **Measure Confidence, Not Just Scores**  <br>   Confidence intervals and variance estimates show whether a sampled result is reliable enough to guide decisions.<br><br>5. **Build Sampling Into the Eval Workflow**  <br>   Use small routine samples for fast iteration and larger samples only for launches, regressions, or high-stakes changes.</td>
<td valign="top">1. Measure less, but keep the signal  <br>Sampling lets you score a smaller set of examples while still estimating whether model quality changed.<br><br>2. Start with the decision you need to make  <br>Choose the sample size based on the change you need to detect, not on the full size of the test set.<br><br>3. Use random sampling to avoid biased results  <br>A random sample gives each example a fair chance to be selected, so the score is more likely to reflect the full test set.<br><br>4. Track uncertainty with confidence intervals  <br>A confidence interval shows the likely range of the true score, so you can see when a result is too close to call.<br><br>5. Spend more only when the result is unclear  <br>Run a small sample first, then score more examples only when the first result cannot support a decision.</td>
</tr>
<tr>
<td colspan="3">
<strong>Support reply</strong>, task 32, 
<code>faq_support</code>. 
The skill won 12 rules, the baseline won 3, and 10 were ties.
</td>
</tr>
<tr>
<td valign="top">Answer this user question helpfully:<br>Why did my export fail with "schema mismatch" after yesterday's deploy?</td>
<td valign="top">Your export likely failed because yesterday’s deploy changed the data schema that the export job expects.<br><br>A “schema mismatch” usually means the exporter expected one set of fields, types, or column names, but the data now has something different. Common causes include:<br><br>- A column was renamed, removed, or added<br>- A field type changed, such as `string` to `integer`, `date` to `timestamp`, or nullable to required<br>- The export template or saved query still references the old schema<br>- A downstream destination, such as a warehouse table or CSV mapping, has not been updated<br>- Cached metadata from before the deploy is still being used<br>- A migration ran partially or failed, leaving the app and database out of sync<br><br>To troubleshoot:<br><br>1. Check the deploy notes or migration diff from yesterday.<br>2. Compare the export’s expected schema with the current database/API schema.<br>3. Look for renamed, remov<br><br>[...]</td>
<td valign="top">Your export likely failed because yesterday's deploy changed the shape of the data that the exporter writes, but the export schema was not updated at the same time.<br><br>A "schema mismatch" means the exporter produced data with fields or types that did not match what the destination expected. For example, the deploy may have added a new field, renamed a field, removed a field, or changed a value from a string to a number. When the destination checked the export against its saved schema, the check failed and the export stopped.<br><br>The most likely causes are:<br><br>- The deploy changed one or more export fields.<br>- The destination still expects the old schema.<br>- A migration or schema update did not run.<br>- The export job picked up mixed data from before and after the deploy.<br>- A cached schema was still in use after the deploy.<br><br>To debug it, check the export logs for the exact field name in the mismatch<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Engineering brief</strong>, task 67, 
<code>project_update</code>. 
The skill won 11 rules, the baseline won 3, and 11 were ties.
</td>
</tr>
<tr>
<td valign="top">Write a short Slack brief for engineering. Cover these facts: search ranking moved from heuristics to a scored model, p95 latency went from 900ms to 220ms, recall on long queries is still untested, the old heuristic path is still in the repo as a fallback, dark mode shipped, the invite link bug is fixed, analytics export is blocked on a schema mismatch, the renderer got some cleanup, and a few small copy edits landed.</td>
<td valign="top">Engineering brief:<br><br>- Search ranking has moved from heuristics to a scored model.<br>- Search p95 latency improved from ~900ms to ~220ms.<br>- Recall on long queries is still untested and needs validation.<br>- The old heuristic ranking path remains in the repo as a fallback.<br>- Dark mode has shipped.<br>- The invite link bug is fixed.<br>- Analytics export is currently blocked on a schema mismatch.<br>- Renderer cleanup landed.<br>- A few small copy edits also went out.</td>
<td valign="top">Search ranking now uses a scored model instead of heuristics, and p95 latency fell from 900 ms to 220 ms. The old heuristic path is still in the repo as a fallback. To do: test recall on long queries.<br><br>Shipped:<br>- Dark mode<br>- Invite link fix<br>- Renderer cleanup<br>- Small copy edits<br><br>Blocked:<br>- Analytics export is blocked on a schema mismatch.</td>
</tr>
</tbody>
</table>
