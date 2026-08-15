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
<td>62 / 3 / 2</td>
</tr>
<tr>
<td>Win rate among decisive tasks</td>
<td>95%</td>
</tr>
<tr>
<td>Rule skill / baseline / tie</td>
<td>707 / 240 / 728</td>
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
<td>62 / 4 / 1 (94%)</td>
</tr>
<tr>
<td>2. No jargon.</td>
<td>52 / 6 / 9 (90%)</td>
</tr>
<tr>
<td>17. Use straight quotes, not curly quotes.</td>
<td>33 / 0 / 34 (100%)</td>
</tr>
<tr>
<td>8. Write complete sentences.</td>
<td>39 / 8 / 20 (83%)</td>
</tr>
<tr>
<td>10. Organize a paragraph as a topic sentence and then support.</td>
<td>43 / 15 / 9 (74%)</td>
</tr>
<tr>
<td>15. No dashes or middle dots.</td>
<td>33 / 5 / 29 (87%)</td>
</tr>
<tr>
<td>19. You can use lists, but do not overuse them.</td>
<td>30 / 2 / 35 (94%)</td>
</tr>
<tr>
<td>4. Stick to the same word; repetition is fine.</td>
<td>46 / 20 / 1 (70%)</td>
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
<td>25. Do not open with a count of things.</td>
<td>6 / 7 / 54 (46%)</td>
</tr>
<tr>
<td>12. Prefer long, explanatory sentences over short, punchy ones.</td>
<td>31 / 35 / 1 (47%)</td>
</tr>
<tr>
<td>11. Never write three or more clauses in one sentence, or three or more example sentences in a row.</td>
<td>27 / 32 / 8 (46%)</td>
</tr>
<tr>
<td>5. It's ok to use contractions.</td>
<td>4 / 10 / 53 (29%)</td>
</tr>
</tbody>
</table>

## Examples

Each row is one writing task. The columns are the original text, the
baseline rewrite (no skill), and the skill-based rewrite. For draft
tasks with no source text, Original is the task prompt. Long texts
are cut after about 320 characters.

<table>
<thead>
<tr>
<th>Original</th>
<th>Baseline (no skill)</th>
<th>Skill-based</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="3">
<strong>Deslopify</strong> · task 01 · 
<code>cache_rollout</code> · 
judge 8-4-13
</td>
</tr>
<tr>
<td valign="top">**Engineering Update: Document Render Cache Deployment**<br><br>We're thrilled to announce a transformative milestone in our infrastructure evolution—the rollout of our next-generation document render cache system.<br><br>This isn't just an optimization; it's a paradigm shift in how we conceptualize content delivery at scale. By i<br><br>[...]</td>
<td valign="top">**Engineering Update: Document Render Cache Deployment**<br><br>We have deployed a new document render cache system.<br><br>The system caches rendered documents so they can be retrieved without being rendered again for every request. This reduces render latency and lowers compute usage for repeated document requests.<br><br>The cache us<br><br>[...]</td>
<td valign="top"># Engineering update: Document render cache deployment<br><br>The document render cache is now live. It stores rendered documents so repeated document requests can return a cached result instead of rendering the same document again.<br><br>The cache is meant to reduce render time and lower compute use. When a user requests a docum<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Public-domain rewrite</strong> · task 12 · 
<code>Eddystone Lighthouse</code> · 
judge 12-2-11
</td>
</tr>
<tr>
<td valign="top">In the latter part of April fifty-three courses of granite masonry, rising to the height of seventy feet above high water, had been laid, and thirty-six courses remained to be set. The old lighthouse had been already overtopped. As the work advances toward completion the question arises: What shall be done with John Sm<br><br>[...]</td>
<td valign="top">By late April, fifty-three layers of granite masonry had been built, reaching seventy feet above the high-water mark, with thirty-six more layers still to be added. The new structure had already risen higher than the old lighthouse.<br><br>As the work neared completion, an important question arose: what should be done with J<br><br>[...]</td>
<td valign="top">By late April, workers had laid fifty-three layers of granite masonry, reaching seventy feet above the high-water mark. Thirty-six layers still had to be set. The new lighthouse had already risen higher than the old one.<br><br>As the work neared completion, people began to ask what should be done with John Smeaton's famous<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Short draft</strong> · task 22 · 
<code>project_update</code> · 
judge 10-6-9
</td>
</tr>
<tr>
<td valign="top">Write a Slack update for engineering: we moved search ranking from heuristics to a scored model, latency went from 900ms to 220ms p95, and we still need to validate recall on long queries.</td>
<td valign="top">Engineering update: We’ve moved search ranking from the previous heuristics-based approach to a scored model.<br><br>Early performance results look strong: p95 latency is down from ~900ms to ~220ms.<br><br>The main remaining validation area is recall on long queries. We’ll continue testing to make sure the new model maintains qual<br><br>[...]</td>
<td valign="top">Search ranking now uses a scored model instead of heuristics, and p95 latency fell from 900 ms to 220 ms. To do: validate recall on long queries.</td>
</tr>
<tr>
<td colspan="3">
<strong>Long history</strong> · task 41 · 
<code>long_history</code> · 
judge 16-4-5
</td>
</tr>
<tr>
<td valign="top">Using only the research-agent history above, write a plain status note for a technical reader with no prior context. Cover: the question being researched, the main search path, the best current answer if any, and what is still uncertain. Keep concrete facts. Return only the note.</td>
<td valign="top">Status note:<br><br>The research question asks: identify a European band formed in the 1990s that released an album in 2019, roughly eight years after its previous release, described as one of the band’s most impressive releases and as an outlier in its record label’s catalog; then determine the full name of the band’s lead,<br><br>[...]</td>
<td valign="top">The research question asks for the full name of the lead of a European band that fits several clues. The band formed in the 1990s, released an album in 2019, released that album about eight years after its previous release, and had the album described as one of its most impressive releases and as an outlier in its reco<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Fable coding</strong> · task 51 · 
<code>csharp-newrelic-synthetic-monitor</code> · 
judge 12-5-8
</td>
</tr>
<tr>
<td valign="top">Done — `dotnet test` passes 15/15, and the only changes are three new files under `src/`: `NerdGraphClient.cs`, `MonitorReconciler.cs`, and `Exceptions.cs` (all in `Acme.NewRelic.Synthetics`). Every protected file, `docs/`, and the starter `src/MonitorModels.cs` are byte-identical to the seed, and no scratch artifacts<br><br>[...]</td>
<td valign="top">Implemented the scripted API monitor reconciler and verified it with the acceptance suite.<br><br>`dotnet test` passes:<br><br>- Failed: 0<br>- Passed: 15<br>- Skipped: 0<br>- Total: 15<br><br>Changed files:<br><br>- Added `src/NerdGraphClient.cs`<br>- Added `src/MonitorReconciler.cs`<br>- Added `src/Exceptions.cs`<br><br>No protected files were changed. `docs/`,<br><br>[...]</td>
<td valign="top">`dotnet test` passes with 15 passing tests and 0 failing tests.<br><br>I added the C# reconciler for New Relic scripted API monitors under `src/`, in the `Acme.NewRelic.Synthetics` namespace. The only new files are:<br><br>- `src/NerdGraphClient.cs`<br>- `src/MonitorReconciler.cs`<br>- `src/Exceptions.cs`<br><br>I did not change `SyntheticMon<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Chat context</strong> · task 66 · 
<code>project_update</code> · 
judge 13-1-11
</td>
</tr>
<tr>
<td valign="top">Reply in chat to a teammate who asked why the document render cache work matters. They are smart but do not have context on the problem, or they forgot it. Give context on the problem and on what was happening before. Then say what changed: the cache now stores already-rendered pages and skips files with no changes.</td>
<td valign="top">The document render cache work matters because rendering docs is one of the more expensive parts of the flow, especially when a document has many pages or when only a small part of it changed. Before this, we were effectively doing more work than needed: even if most of the document was unchanged, we would still re-ren<br><br>[...]</td>
<td valign="top">The document renderer was doing the same work again each time someone opened or refreshed a document. Even if most files had not changed, the renderer still read them and rendered the pages again, so repeated views were slower than they needed to be.<br><br>The cache work cuts out that repeated work. The cache now stores pag<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Short lists</strong> · task 67 · 
<code>project_update</code> · 
judge 7-2-16
</td>
</tr>
<tr>
<td valign="top">Write a short Slack brief for engineering. Cover these facts: search ranking moved from heuristics to a scored model, p95 latency went from 900ms to 220ms, recall on long queries is still untested, the old heuristic path is still in the repo as a fallback, dark mode shipped, the invite link bug is fixed, analytics expo<br><br>[...]</td>
<td valign="top">Engineering brief:<br><br>- Search ranking has moved from heuristics to a scored model.<br>- p95 latency improved from 900ms to 220ms.<br>- Recall on long queries is still untested.<br>- The old heuristic ranking path is still in the repo as a fallback.<br>- Dark mode shipped.<br>- Invite link bug is fixed.<br>- Analytics export is currently<br><br>[...]</td>
<td valign="top">Search ranking now uses a scored model instead of heuristics, and p95 latency fell from 900 ms to 220 ms. Recall on long queries is still untested. The old heuristic path is still in the repo as a fallback.<br><br>Shipped:<br>- Dark mode<br>- Invite link bug fix<br>- Renderer cleanup<br>- Small copy edits<br><br>Blocked:<br>- Analytics export is<br><br>[...]</td>
</tr>
</tbody>
</table>
