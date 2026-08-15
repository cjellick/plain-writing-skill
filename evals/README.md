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

History items load a conversation from `sources/` and append the
item prompt as the last user turn. Fable traces are rebuilt with
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

For each piece of writing, we compare the two texts on every rule in
`SKILL.md`. The judge does not know which text used the skill. The skill
wins the item if it wins more rules. We also add up those rule wins
across items.

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
`outputs/` and are gitignored. `write_readme.py` combines the item
files from those folders and writes this README.

## Latest results

Combined from `67` of `67` items.

| Metric | Result |
| --- | --- |
| Items | 67 |
| Skill wins / baseline wins / ties | 62 / 3 / 2 |
| Item win rate among decisive | 95% |
| Criterion skill / baseline / tie | 707 / 240 / 728 |
| Criterion win rate among decisive | 75% |
| Errors | 0 |
| Rewriter / judge | gpt-5.5 / gpt-5.5 |

### Rules with the largest gap

| Rule | Skill / baseline / tie | Skill win rate |
| --- | --- | --- |
| 1. Use simple, everyday words. | 62 / 4 / 1 | 94% |
| 2. No jargon. | 52 / 6 / 9 | 90% |
| 17. Use straight quotes, not curly quotes. | 33 / 0 / 34 | 100% |
| 8. Write complete sentences. | 39 / 8 / 20 | 83% |
| 10. Organize a paragraph as a topic sentence and then support. | 43 / 15 / 9 | 74% |
| 15. No dashes or middle dots. | 33 / 5 / 29 | 87% |
| 19. You can use lists, but do not overuse them. | 30 / 2 / 35 | 94% |
| 4. Stick to the same word; repetition is fine. | 46 / 20 / 1 | 70% |

Rules where the baseline won more often:

| Rule | Skill / baseline / tie | Skill win rate |
| --- | --- | --- |
| 25. Do not open with a count of things. | 6 / 7 / 54 | 46% |
| 12. Prefer long, explanatory sentences over short, punchy ones. | 31 / 35 / 1 | 47% |
| 11. Never write three or more clauses in one sentence, or three or more example sentences in a row. | 27 / 32 / 8 | 46% |
| 5. It's ok to use contractions. | 4 / 10 / 53 | 29% |

## Examples

Each row is one example. The columns are the original text, the
baseline rewrite (no skill), and the skill-based rewrite. For draft
tasks with no source text, Original is the task prompt. Long texts
are cut after about 900 characters.

<table>
<thead>
<tr>
<th>Example</th>
<th>Original</th>
<th>Baseline-rewritten (no skill)</th>
<th>Skill-based rewritten</th>
</tr>
</thead>
<tbody>
<tr>
<td valign="top">
<strong>Deslopify</strong><br>
item 01 (<code>cache_rollout</code>)<br>
Judge: True (8-4-13)
</td>
<td valign="top">

<pre>**Engineering Update: Document Render Cache Deployment**

We're thrilled to announce a transformative milestone in our infrastructure evolution—the rollout of our next-generation document render cache system.

This isn't just an optimization; it's a paradigm shift in how we conceptualize content delivery at scale. By intelligently caching rendered documents, we're fundamentally reimagining the relationship between computation and retrieval. What does this mean for our users? Simply put: experiences that transcend traditional performance boundaries.

The architecture leverages a sophisticated multi-tier caching strategy—not just storing documents, but dynamically orchestrating their lifecycle across distributed nodes. Through this approach, we're able to dramatically reduce render times while simultaneously optimizing resource utilization. It's about working smarter, not harder.

Consider

[...]</pre>

</td>
<td valign="top">

<pre>**Engineering Update: Document Render Cache Deployment**

We have deployed a new document render cache system.

The system caches rendered documents so they can be retrieved without being rendered again for every request. This reduces render latency and lowers compute usage for repeated document requests.

The cache uses a multi-tier architecture across distributed nodes. It manages the lifecycle of cached rendered documents across those tiers, rather than storing them in a single location.

For users, the expected result is faster document loading. For the infrastructure, the expected result is reduced rendering work and better resource utilization.

The system was designed to be extensible so it can support changing demand over time. It also uses actual usage patterns to optimize cache behavior.

Early metrics show render latency reductions that are better than the initial projections.

[...]</pre>

</td>
<td valign="top">

<pre># Engineering update: Document render cache deployment

The document render cache is now live. It stores rendered documents so repeated document requests can return a cached result instead of rendering the same document again.

The cache is meant to reduce render time and lower compute use. When a user requests a document, the system can use a previously rendered version if the document has not changed. If the cached version is missing or out of date, the system renders the document and can store the new result for later requests.

The system uses a multi-tier cache across distributed nodes. It manages cached document entries across those nodes and uses actual request patterns to decide what to keep. The goal is to make common document requests faster while avoiding unnecessary rendering work.

Early metrics show better performance than expected. Render latency has dropped more than the

[...]</pre>

</td>
</tr>
<tr>
<td valign="top">
<strong>Public-domain rewrite</strong><br>
item 12 (<code>Eddystone Lighthouse</code>)<br>
Judge: True (12-2-11)
</td>
<td valign="top">

<pre>In the latter part of April fifty-three courses of granite masonry, rising to the height of seventy feet above high water, had been laid, and thirty-six courses remained to be set. The old lighthouse had been already overtopped. As the work advances toward completion the question arises: What shall be done with John Smeaton's famous tower, which has done such admirable service for 120 years? One proposition is to take it down to the level of the top of the solid portion, and leave the rest as a perpetual memorial of the great work which Smeaton accomplished in the face of obstacles vastly greater than those which confront the modern architect. The London News says: "Were Smeaton's beautiful tower to be literally consigned to the waves, we should regard the act as a national calamity, not to say scandal; and, if public funds are not available for its conservation, we trust that private ze

[...]</pre>

</td>
<td valign="top">

<pre>By late April, fifty-three layers of granite masonry had been built, reaching seventy feet above the high-water mark, with thirty-six more layers still to be added. The new structure had already risen higher than the old lighthouse.

As the work neared completion, an important question arose: what should be done with John Smeaton’s famous tower, which had served so well for 120 years? One proposal was to dismantle it down to the top of its solid base and leave that part standing as a permanent memorial to Smeaton’s great achievement, built despite obstacles far greater than those faced by modern architects.

The London News wrote: “If Smeaton’s beautiful tower were simply abandoned to the sea, we would consider it a national disaster, even a disgrace. If public money is not available to preserve it, we hope private enthusiasm and generosity will save this important historic structure fro

[...]</pre>

</td>
<td valign="top">

<pre>By late April, workers had laid fifty-three layers of granite masonry, reaching seventy feet above the high-water mark. Thirty-six layers still had to be set. The new lighthouse had already risen higher than the old one.

As the work neared completion, people began to ask what should be done with John Smeaton's famous tower, which had served well for 120 years. One proposal was to take it down to the top of its solid base and leave the rest as a permanent memorial to Smeaton's achievement. He had built it despite obstacles far greater than those faced by modern architects.

The London News said that destroying Smeaton's beautiful tower would be a national loss, and even a public disgrace. If public money could not be used to preserve it, the paper hoped that private effort and donations would save the important relic from destruction. The paper also said it should not cost much to move t

[...]</pre>

</td>
</tr>
<tr>
<td valign="top">
<strong>Short draft</strong><br>
item 22 (<code>project_update</code>)<br>
Judge: True (10-6-9)
</td>
<td valign="top">

<pre>Write a Slack update for engineering: we moved search ranking from heuristics to a scored model, latency went from 900ms to 220ms p95, and we still need to validate recall on long queries.</pre>

</td>
<td valign="top">

<pre>Engineering update: We’ve moved search ranking from the previous heuristics-based approach to a scored model.

Early performance results look strong: p95 latency is down from ~900ms to ~220ms.

The main remaining validation area is recall on long queries. We’ll continue testing to make sure the new model maintains quality across those cases before we consider the rollout fully complete.</pre>

</td>
<td valign="top">

<pre>Search ranking now uses a scored model instead of heuristics, and p95 latency fell from 900 ms to 220 ms. To do: validate recall on long queries.</pre>

</td>
</tr>
<tr>
<td valign="top">
<strong>Long history</strong><br>
item 41 (<code>long_history</code>)<br>
Judge: True (16-4-5)
</td>
<td valign="top">

<pre>Using only the research-agent history above, write a plain status note for a technical reader with no prior context. Cover: the question being researched, the main search path, the best current answer if any, and what is still uncertain. Keep concrete facts. Return only the note.</pre>

</td>
<td valign="top">

<pre>Status note:

The research question asks: identify a European band formed in the 1990s that released an album in 2019, roughly eight years after its previous release, described as one of the band’s most impressive releases and as an outlier in its record label’s catalog; then determine the full name of the band’s lead, who is from a region of a country whose autonomy was suspended for more than six months.

Main search path:
- Initial searches explored 2019 albums by European rock/metal bands, especially those with long gaps since prior releases.
- Candidates checked included Alcest, Sunn O))), Cult of Luna, Brutus, Rammstein, Leprous, Therapy?, and others.
- The strongest recurring candidate investigated was Cult of Luna and its 2019 album *A Dawn to Fear*, because:
  - Cult of Luna is a Swedish band formed in 1998.
  - *A Dawn to Fear* was released in 2019, one year before the major CO

[...]</pre>

</td>
<td valign="top">

<pre>The research question asks for the full name of the lead of a European band that fits several clues. The band formed in the 1990s, released an album in 2019, released that album about eight years after its previous release, and had the album described as one of its most impressive releases and as an outlier in its record label's catalog. The lead is from a region of a country whose autonomy was suspended for more than half a year.

The main search path focused first on 2019 European rock and metal albums with long gaps after a prior release. Searches checked possible matches, including Alcest, Sunn O))), Cult of Luna, Rammstein, Leprous, Therapy?, and other European bands. The strongest repeated candidate in the search history was Cult of Luna, because the band is European, formed in 1998, released "A Dawn to Fear" in 2019, and is linked to Metal Blade Records. Searches also looked for t

[...]</pre>

</td>
</tr>
<tr>
<td valign="top">
<strong>Fable coding</strong><br>
item 51 (<code>csharp-newrelic-synthetic-monitor</code>)<br>
Judge: True (12-5-8)
</td>
<td valign="top">

<pre>Done — `dotnet test` passes 15/15, and the only changes are three new files under `src/`: `NerdGraphClient.cs`, `MonitorReconciler.cs`, and `Exceptions.cs` (all in `Acme.NewRelic.Synthetics`). Every protected file, `docs/`, and the starter `src/MonitorModels.cs` are byte-identical to the seed, and no scratch artifacts were left behind.

How the implementation addresses the outstanding review findings, alongside the pinned contract:

- **Transport** (`src/NerdGraphClient.cs`): POSTs exactly `{query, variables}` as `application/json` with the `API-Key` header; the key never touches the URL or body. HTTP 429 retries through the injected delay with 1s then 2s waits for at most three total attempts, then `NerdGraphHttpException(.Status)`; other non-2xx statuses surface immediately.
- **Key redaction** (finding: reflected-key leak): the raw response body is scrubbed of the API key at the trans

[...]</pre>

</td>
<td valign="top">

<pre>Implemented the scripted API monitor reconciler and verified it with the acceptance suite.

`dotnet test` passes:

- Failed: 0
- Passed: 15
- Skipped: 0
- Total: 15

Changed files:

- Added `src/NerdGraphClient.cs`
- Added `src/MonitorReconciler.cs`
- Added `src/Exceptions.cs`

No protected files were changed. `docs/`, `SyntheticMonitorTests.cs`, `SyntheticMonitor.csproj`, `.gitignore`, and the starter `src/MonitorModels.cs` remain unchanged.

Summary of the implementation:

- `NerdGraphClient` sends NerdGraph requests as HTTP `POST` with a JSON body containing only `query` and `variables`.
- It authenticates with the documented `API-Key` header.
- The API key is never placed in the URL or request body.
- HTTP 429 responses retry through the injected delay function with 1-second and 2-second delays, for three total attempts.
- Exhausted retries and other non-2xx responses throw `NerdGrap

[...]</pre>

</td>
<td valign="top">

<pre>`dotnet test` passes with 15 passing tests and 0 failing tests.

I added the C# reconciler for New Relic scripted API monitors under `src/`, in the `Acme.NewRelic.Synthetics` namespace. The only new files are:

- `src/NerdGraphClient.cs`
- `src/MonitorReconciler.cs`
- `src/Exceptions.cs`

I did not change `SyntheticMonitorTests.cs`, `SyntheticMonitor.csproj`, `.gitignore`, any file under `docs/`, or `src/MonitorModels.cs`. Git status showed only the three new source files.

## What changed

`NerdGraphClient` implements the NerdGraph HTTP transport.

It sends one GraphQL document per request as JSON with exactly these top-level fields:

- `query`
- `variables`

It sends requests with `Content-Type: application/json` and the documented `API-Key` header. The API key is not placed in the URL or request body.

It retries HTTP 429 responses with the injected delay function. The retry delays ar

[...]</pre>

</td>
</tr>
<tr>
<td valign="top">
<strong>Chat context</strong><br>
item 66 (<code>project_update</code>)<br>
Judge: True (13-1-11)
</td>
<td valign="top">

<pre>Reply in chat to a teammate who asked why the document render cache work matters. They are smart but do not have context on the problem, or they forgot it. Give context on the problem and on what was happening before. Then say what changed: the cache now stores already-rendered pages and skips files with no changes.</pre>

</td>
<td valign="top">

<pre>The document render cache work matters because rendering docs is one of the more expensive parts of the flow, especially when a document has many pages or when only a small part of it changed. Before this, we were effectively doing more work than needed: even if most of the document was unchanged, we would still re-render pages/files that had already been rendered previously.

That meant repeated renders could be slower than necessary, and small edits could still trigger a lot of avoidable work.

What changed is that the cache now stores already-rendered pages, not just intermediate inputs/state, and we skip files that have no changes. So if a file or page has not changed, we can reuse the previous rendered output instead of rendering it again. This should make repeated document renders much faster and reduce unnecessary processing.</pre>

</td>
<td valign="top">

<pre>The document renderer was doing the same work again each time someone opened or refreshed a document. Even if most files had not changed, the renderer still read them and rendered the pages again, so repeated views were slower than they needed to be.

The cache work cuts out that repeated work. The cache now stores pages after they have already been rendered, and the renderer skips files that have no changes. As a result, repeated renders should be faster, especially for documents where only a few files changed.</pre>

</td>
</tr>
<tr>
<td valign="top">
<strong>Short lists</strong><br>
item 67 (<code>project_update</code>)<br>
Judge: True (7-2-16)
</td>
<td valign="top">

<pre>Write a short Slack brief for engineering. Cover these facts: search ranking moved from heuristics to a scored model, p95 latency went from 900ms to 220ms, recall on long queries is still untested, the old heuristic path is still in the repo as a fallback, dark mode shipped, the invite link bug is fixed, analytics export is blocked on a schema mismatch, the renderer got some cleanup, and a few small copy edits landed.</pre>

</td>
<td valign="top">

<pre>Engineering brief:

- Search ranking has moved from heuristics to a scored model.
- p95 latency improved from 900ms to 220ms.
- Recall on long queries is still untested.
- The old heuristic ranking path is still in the repo as a fallback.
- Dark mode shipped.
- Invite link bug is fixed.
- Analytics export is currently blocked on a schema mismatch.
- Renderer cleanup landed.
- A few small copy edits also landed.</pre>

</td>
<td valign="top">

<pre>Search ranking now uses a scored model instead of heuristics, and p95 latency fell from 900 ms to 220 ms. Recall on long queries is still untested. The old heuristic path is still in the repo as a fallback.

Shipped:
- Dark mode
- Invite link bug fix
- Renderer cleanup
- Small copy edits

Blocked:
- Analytics export is blocked on a schema mismatch.</pre>

</td>
</tr>
</tbody>
</table>
