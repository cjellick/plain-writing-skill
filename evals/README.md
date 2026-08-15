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
<strong>Deslopify</strong> · task 01 · 
<code>cache_rollout</code> · 
judge 9-5-11
</td>
</tr>
<tr>
<td valign="top">**Engineering Update: Document Render Cache Deployment**<br><br>We're thrilled to announce a transformative milestone in our infrastructure evolution—the rollout of our next-generation document render cache system.<br><br>This isn't just an optimization; it's a paradigm shift in how we conceptualize content delivery at scale. By i<br><br>[...]</td>
<td valign="top">**Engineering Update: Document Render Cache Deployment**<br><br>We have deployed a new document render cache system.<br><br>The system caches rendered versions of documents so repeated requests can be served from cache instead of rendering the document again. This reduces render latency and lowers compute usage.<br><br>The cache uses a<br><br>[...]</td>
<td valign="top"># Engineering update: document render cache deployment<br><br>The document render cache is now live. It stores rendered documents so repeated document requests can return faster and use less compute.<br><br>Before this change, the system had to render more documents during request handling. The new cache stores rendered output and<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Public-domain rewrite</strong> · task 12 · 
<code>Eddystone Lighthouse</code> · 
judge 11-2-12
</td>
</tr>
<tr>
<td valign="top">In the latter part of April fifty-three courses of granite masonry, rising to the height of seventy feet above high water, had been laid, and thirty-six courses remained to be set. The old lighthouse had been already overtopped. As the work advances toward completion the question arises: What shall be done with John Sm<br><br>[...]</td>
<td valign="top">By late April, fifty-three layers of granite masonry had been built, reaching seventy feet above the high-water mark, with thirty-six more layers still to be added. The new lighthouse had already risen higher than the old one.<br><br>As the work neared completion, people began asking what should be done with John Smeaton’s f<br><br>[...]</td>
<td valign="top">By late April, workers had laid fifty-three layers of granite masonry. The new lighthouse had reached seventy feet above the high water mark, and thirty-six layers still had to be added. It had already risen higher than the old lighthouse.<br><br>As the work nears completion, people are asking what should be done with John S<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Fable coding</strong> · task 51 · 
<code>csharp-newrelic-synthetic-monitor</code> · 
judge 14-4-7
</td>
</tr>
<tr>
<td valign="top">Done — `dotnet test` passes 15/15, and the only changes are three new files under `src/`: `NerdGraphClient.cs`, `MonitorReconciler.cs`, and `Exceptions.cs` (all in `Acme.NewRelic.Synthetics`). Every protected file, `docs/`, and the starter `src/MonitorModels.cs` are byte-identical to the seed, and no scratch artifacts<br><br>[...]</td>
<td valign="top">Implemented the C# reconciler and verified it with the acceptance tests.<br><br>`dotnet test` passes: 15 passed, 0 failed.<br><br>Changed files:<br><br>- Added `src/NerdGraphClient.cs`<br>- Added `src/MonitorReconciler.cs`<br>- Added `src/Exceptions.cs`<br><br>All new code is under the `Acme.NewRelic.Synthetics` namespace. I did not modify protecte<br><br>[...]</td>
<td valign="top">`dotnet test` passes. The suite ran 15 tests, and all 15 passed.<br><br>The only changed files are new source files under `src/`:<br><br>- `src/NerdGraphClient.cs`<br>- `src/MonitorReconciler.cs`<br>- `src/Exceptions.cs`<br><br>All new code is in the `Acme.NewRelic.Synthetics` namespace. I did not change `SyntheticMonitorTests.cs`, `Synthetic<br><br>[...]</td>
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
<strong>Short draft</strong> · task 22 · 
<code>project_update</code> · 
judge 12-6-7
</td>
</tr>
<tr>
<td valign="top">Write a Slack update for engineering: we moved search ranking from heuristics to a scored model, latency went from 900ms to 220ms p95, and we still need to validate recall on long queries.</td>
<td valign="top">Hey team — quick search update:<br><br>We’ve moved search ranking from the previous heuristics-based approach to a scored model. Early performance results look strong: p95 latency is down from ~900ms to ~220ms.<br><br>The main remaining validation area is recall on long queries. We’ll continue testing to make sure the new model pr<br><br>[...]</td>
<td valign="top">Search ranking now uses a scored model instead of heuristics, and p95 latency fell from 900 ms to 220 ms.<br><br>To do: validate recall on long queries.</td>
</tr>
<tr>
<td colspan="3">
<strong>Long history</strong> · task 41 · 
<code>long_history</code> · 
judge 11-4-10
</td>
</tr>
<tr>
<td valign="top">Using only the research-agent history above, write a plain status note for a technical reader with no prior context. Cover: the question being researched, the main search path, the best current answer if any, and what is still uncertain. Keep concrete facts. Return only the note.</td>
<td valign="top">Research question: identify the full name of the lead of a European band formed in the 1990s. Clues: the band released an album in 2019, a year before major COVID lockdowns; the album came roughly eight years after the band’s previous release; it was described as one of the band’s most impressive releases and as an out<br><br>[...]</td>
<td valign="top">The research question asks for the full name of the lead of a European band. The band was formed in the 1990s, released an album in 2019, released that album about eight years after its previous release, and had the album described as an outlier in its record label's catalog. The lead is from a region of a country whos<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Chat context</strong> · task 66 · 
<code>project_update</code> · 
judge 13-2-10
</td>
</tr>
<tr>
<td valign="top">Reply in chat to a teammate who asked why the document render cache work matters. They are smart but do not have context on the problem, or they forgot it. Give context on the problem and on what was happening before. Then say what changed: the cache now stores already-rendered pages and skips files with no changes.</td>
<td valign="top">The document render cache work matters because rendering a document is one of the more expensive parts of the flow, especially for larger files or repeated operations on the same file. Before this, we were effectively doing more work than necessary: even if a document had already been rendered, or if a file had not cha<br><br>[...]</td>
<td valign="top">The document renderer was doing the same work every time, even when the source files had not changed. That made repeated renders slower than they needed to be, especially for larger documents.<br><br>The cache now stores pages after they are rendered. On the next render, it reuses the stored page when the source file has no<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Short lists</strong> · task 67 · 
<code>project_update</code> · 
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
