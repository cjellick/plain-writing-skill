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
The first column is the full original writing for a rewrite, and
the prompt for a write-from-scratch task. The baseline and skill
columns are cut after about 1800 characters.

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
<td valign="top">**Introducing CodeClarify™: The Plain-Writing Revolution for Your AI Agents**<br><br>We're not just teaching agents to code—we're teaching them to *communicate*.<br><br>Meet **Semantic Simplicity Engine**, the breakthrough capability that transforms your coding agents from technical translators into plain-language virtuosos. Because code that humans can't understand is code that can't scale.<br><br>**The Problem:** Your AI writes functions flawlessly but explains them like encrypted hieroglyphics.<br><br>**The Solution:** CodeClarify—where precision meets accessibility.<br><br>This isn't mere documentation. It's **contextual clarity engineering**. Our agents now deploy the Plain-Writing Protocol™, converting complex logic into digestible narratives that stakeholders, junior developers, and cross-functional teams actually comprehend. Think of it as a universal adapter for technical knowledge—bridging the gap between machine efficiency and human understanding.<br><br>**Key capabilities include:**<br><br>- **Jargon-to-English Translation Matrix**: Technical concepts rendered in everyday language<br>- **Assumption Unpacking**: No more "obvious" steps that leave readers stranded<br>- **Active Voice Prioritization**: Direct, vigorous, clear<br>- **Cognitive Load Reduction**: Information architecture that respects human processing limits<br><br>The result? Documentation that doesn't require a decoder ring. Onboarding that takes hours—not weeks. Codebases that welcome contribution instead of gatekeeping knowledge.<br><br>**This is writing that works.**<br><br>Because the future belongs not just to agents that can build systems, but to agents that can explain them. CodeClarify turns every AI into a teacher, every commit into a conversation, every repository into a learning environment.<br><br>*Plain writing. Profound impact. Powered by AI.*</td>
<td valign="top">**Introducing CodeClarify™: Plain Writing for AI Coding Agents**<br><br>CodeClarify helps AI coding agents explain code clearly, not just write it.<br><br>The **Semantic Simplicity Engine** is a capability that converts technical explanations into plain language. It helps agents describe complex code, logic, and design decisions in a way that stakeholders, junior developers, and cross-functional teams can understand.<br><br>**The problem:** AI agents can write correct functions, but their explanations are often hard to follow.<br><br>**The solution:** CodeClarify makes technical communication more precise and accessible.<br><br>This goes beyond basic documentation. CodeClarify uses a **Plain-Writing Protocol™** to turn complex logic into clear explanations. It fills in missing context, avoids unnecessary jargon, and organizes information so readers can understand what the code does, why it works that way, and how to work with it.<br><br>**Key capabilities include:**<br><br>- **Jargon-to-English Translation Matrix:** Explains technical concepts in everyday language<br>- **Assumption Unpacking:** Makes implicit steps and background context explicit<br>- **Active Voice Prioritization:** Uses direct, clear sentence structure<br>- **Cognitive Load Reduction:** Organizes information so it is easier to process<br><br>The result is documentation that is easier to read and use. Teams can onboard faster, understand codebases more easily, and contribute without needing hidden background knowledge.<br><br>CodeClarify helps AI agents act not only as system builders, but also as clear technical communicators. It turns code explanations, commits, and repositories into learning resources.<br><br>*Plain writing. Powered by AI.*</td>
<td valign="top">CodeClarify is a plain writing feature for AI coding agents. It helps agents explain code and technical decisions in clear, everyday language.<br><br>AI coding agents can write working functions, but their explanations can be hard to understand. CodeClarify addresses that problem by making the agent explain what the code does, why it does it, and what assumptions the reader needs to know.<br><br>CodeClarify applies plain writing rules to agent output. The agent avoids unclear technical language when a simple word works, explains required technical terms, and spells out steps that might otherwise be treated as obvious. The agent also prefers active voice, so the explanation says who or what does each action.<br><br>The feature is meant to make technical writing easier to use for several groups, including stakeholders, junior developers, and teams outside engineering. For example, it can turn a complex implementation note into a plain explanation of the logic, the inputs, the outputs, and the tradeoffs.<br><br>Key capabilities include:<br><br>- Jargon replacement: The agent rewrites technical terms in everyday language when precision does not require the original term.<br>- Assumption explanation: The agent states background facts and missing steps that a new reader may need.<br>- Active voice: The agent writes direct sentences that make the actor and action clear.<br>- Clear structure: The agent organizes information so readers can follow the explanation without extra effort.<br><br>The expected result is documentation that is easier to read, onboarding material that takes less time to understand, and codebases that are easier for new contributors to work with. CodeClarify helps AI agents produce code and explain that code in a way people can use.</td>
</tr>
<tr>
<td colspan="3">
<strong>Slide script</strong>, task 08, 
<code>slides_script</code>. 
The skill won 17 rules, the baseline won 2, and 6 were ties.
</td>
</tr>
<tr>
<td valign="top"># Crushing Eval Costs: The Sampling Revolution<br><br>**The Problem Space**<br>Full dataset evaluation. Expensive. Prohibitive. Your burn rate? Astronomical. Every benchmark run: hundreds of dollars. Thousands. Enterprise scale? Forget it.<br><br>**Enter: Strategic Sampling**<br>We're not testing every grain of sand to understand the beach. Smart sampling. Statistical rigor meets economic reality.<br><br>**The Math Checks Out**<br>95% confidence intervals. Representative subsets. 10% of data, 98% of insights. The magic of statistics working FOR you, not against you.<br><br>**Real-World Impact**<br>- 10x cost reduction, immediate<br>- Faster iteration cycles<br>- More experiments, same budget<br>- Hyperparameter sweeps suddenly affordable<br><br>**The Stratification Advantage**<br>Slice your data smartly. Category-aware sampling. Preserve distribution characteristics. Quality signals maintained. Performance metrics: stable.<br><br>**Confidence Without Compromise**<br>Error bounds you can trust. Margin-of-error transparency. Know exactly what you're trading. Spoiler: it's less than you think.<br><br>**Implementation Velocity**<br>One afternoon. Seriously. Wrap your eval pipeline. Add sampling layer. Deploy. Watch costs crater while insights flow.<br><br>**The Compounding Effect**<br>More experiments → better models → faster shipping → competitive advantage. The sampling decision isn't about saving money. It's about unlocking velocity you couldn't afford before.<br><br>**Scale Implications**<br>When evaluation cost approaches zero, everything changes. Test ruthlessly. Validate constantly. Fail fast, learn faster.<br><br>**Bottom Line**<br>Full evaluation: the luxury you don't need. Smart sampling: the superpower you can't ignore. Your infrastructure team will thank you. Your CFO will REALLY thank you.</td>
<td valign="top"># Reducing Evaluation Costs with Strategic Sampling<br><br>## Problem<br><br>Running evaluations on a full dataset can be expensive. A single benchmark run may cost hundreds or thousands of dollars, and at enterprise scale the cost can become prohibitive. This limits how often teams can evaluate models, run experiments, or perform hyperparameter sweeps.<br><br>## Approach: Strategic Sampling<br><br>Instead of evaluating every example in the dataset, evaluate a statistically representative subset. The goal is to preserve the signal needed to make reliable decisions while reducing evaluation cost and runtime.<br><br>For example, evaluating 10% of the data may provide roughly 98% of the actionable insight, assuming the sample is representative and the evaluation is designed correctly.<br><br>## Statistical Basis<br><br>Sampling can provide reliable estimates when paired with statistical rigor:<br><br>- Use representative subsets of the full dataset.<br>- Report 95% confidence intervals.<br>- Track margins of error.<br>- Make the tradeoff between cost and precision explicit.<br><br>This allows teams to understand how much uncertainty is introduced by sampling and whether that uncertainty is acceptable for the decision being made.<br><br>## Stratified Sampling<br><br>Stratification improves sample quality by preserving important dataset characteristics. Instead of sampling uniformly at random, split the data by meaningful categories and sample within each group.<br><br>This helps maintain:<br><br>- Category distribution<br>- Important edge cases<br>- Quality signals<br>- Stable performance metrics<br><br>Category-aware sampling is especially useful when some segments are rare but important.<br><br>## Impact<br><br>Strategic sampling can produce immediate operational benefits:<br><br>- Up to 10x reduction in evaluation cost<br>- Faster evaluation cycles<br>- More experiments with the same budget<br>- M<br><br>[...]</td>
<td valign="top"># Reduce evaluation costs with sampling<br><br>Full dataset evaluation can be expensive. A benchmark run can cost hundreds or thousands of dollars, and the cost can block frequent evaluation at enterprise scale.<br><br>Sampling reduces evaluation cost by running the evaluation on a representative subset of the dataset instead of the full dataset. For example, you can evaluate 10 percent of the data and still capture about 98 percent of the signal, if the sample is representative and the error bounds are acceptable.<br><br>The statistical goal is to estimate the full dataset result with a known confidence level. For example, a 95 percent confidence interval gives a range that is likely to contain the true full dataset score. The margin of error shows how much uncertainty the sample adds.<br><br>Stratified sampling can make the estimate more reliable. With stratified sampling, you split the dataset by important categories and sample from each category. That helps preserve the dataset distribution and keeps quality signals and performance metrics stable.<br><br>Sampling changes the cost of iteration. It can cut evaluation cost by about 10x, make evaluation runs faster, and let the same budget cover more experiments. Hyperparameter sweeps also become more practical, because each trial costs less to evaluate.<br><br>Implementation can be simple. First, wrap the existing evaluation pipeline. Second, add a sampling step before evaluation. Third, report the score with its confidence interval and margin of error. The concrete work can fit into an afternoon if the pipeline is already well structured.<br><br>Sampling does trade accuracy for cost, but the tradeoff is measurable. You should report the sample size, sampling method, confidence interval, and margin of error with each result. With those values, reviewers can de<br><br>[...]</td>
</tr>
<tr>
<td colspan="3">
<strong>Product memo</strong>, task 02, 
<code>eval_harness</code>. 
The skill won 21 rules, the baseline won 2, and 2 were ties.
</td>
</tr>
<tr>
<td valign="top">**PRODUCT MEMO: PROMETHEAN EVAL HARNESS**<br><br>**RE: Operationalizing PM Intuition Through Systematic LLM Validation**<br><br>We're at an inflection point. Product teams ship features. Engineering teams ship code. But who validates the *intelligence layer*? <br><br>Enter **Promethean**: the first eval harness purpose-built for Product Managers navigating the LLM landscape. Think of it as your "CI/CD pipeline for prompt quality"—continuous validation that transforms vibes-based AI assessment into data-driven conviction.<br><br>Here's the unlock: PMs currently lack systematic frameworks to evaluate model outputs. Is GPT-4 actually better for your use case? Does Claude handle edge cases more gracefully? What about latency-quality tradeoffs? These questions live in Slack threads and gut feelings, creating a **validation gap** that blocks confident shipping.<br><br>Promethean introduces **Confidence Scaffolding™**—a three-layer evaluation architecture:<br><br>1. **Behavioral Benchmarks**: Pre-configured test suites measuring reasoning, safety, and domain accuracy<br>2. **Vibe Metrics**: Quantified brand-voice alignment and tonal consistency scoring  <br>3. **Outcome Telemetry**: Real user preference data feeding back into your eval loop<br><br>But here's where it gets interesting. Traditional eval harnesses require ML expertise. Promethean abstracts complexity through natural language test authoring. Write evals like user stories. No Python required.<br><br>The paradigm shift? **Democratized model governance**. When PMs own evaluation, the entire product development cycle compresses. Iteration velocity increases. Shipping confidence compounds.<br><br>This isn't about replacing data science—it's about empowering the fastest-moving function in your org with the same rigor engineers expect from unit tests.<br><br>The question isn't whether to eval. It's whether you're ready to operationalize judgment at scale.</td>
<td valign="top">**Product Memo: Promethean Eval Harness**<br><br>**Subject: A validation tool for product managers building with LLMs**<br><br>Product teams ship features. Engineering teams ship code. But LLM-based products also need a reliable way to validate model behavior: output quality, safety, reasoning, latency, tone, and fit for the intended use case.<br><br>**Promethean** is an evaluation harness designed for Product Managers working with large language models. It provides a structured way to test prompts, compare models, and monitor output quality over time. In practice, it acts like a CI/CD pipeline for prompt and model quality: a repeatable validation process that replaces informal judgment with measurable evidence.<br><br>Today, PMs often do not have a systematic framework for evaluating LLM outputs. Questions such as these are usually answered through ad hoc reviews, Slack discussions, or intuition:<br><br>- Is GPT-4 better than another model for this specific workflow?<br>- Does Claude handle the product’s edge cases more reliably?<br>- How much quality is lost when optimizing for lower latency?<br>- Does the model consistently match the product’s brand voice?<br>- Are users actually satisfied with the model’s responses?<br><br>This creates a validation gap that makes it harder to ship LLM features with confidence.<br><br>Promethean addresses this gap with a three-layer evaluation architecture called **Confidence Scaffolding™**:<br><br>1. **Behavioral Benchmarks**  <br>   Pre-configured test suites that measure reasoning, safety, and domain accuracy.<br><br>2. **Vibe Metrics**  <br>   Quantified scoring for brand-voice alignment and tonal consistency.<br><br>3. **Outcome Telemetry**  <br>   Real user preference data that feeds back into the evaluation loop.<br><br>Unlike traditional evaluation harnesses, which often require machine learning expertise or Py<br><br>[...]</td>
<td valign="top"># Product memo: Promethean eval harness<br><br>Product teams need a consistent way to evaluate LLM outputs before they ship features that depend on them.<br><br>Product managers often compare model outputs in Slack threads or by personal judgment. For example, they may need to decide whether GPT 4 is better than Claude for a specific use case, whether a model handles edge cases well, or whether a slower model gives better answers. Without a shared test process, teams have less confidence when they choose a model or change a prompt.<br><br>Promethean is an evaluation harness for product managers who work on LLM features. An evaluation harness is a tool that runs tests against model outputs and reports the results. Promethean helps product managers test prompt quality, model behavior, safety, domain accuracy, brand voice, tone, latency, and user preference.<br><br>Promethean has three evaluation layers:<br><br>1. Behavioral benchmarks<br>   Prebuilt test suites measure reasoning, safety, and domain accuracy.<br><br>2. Vibe metrics<br>   Scores measure whether model outputs match the product's brand voice and tone.<br><br>3. Outcome telemetry<br>   Real user preference data feeds back into the evaluation process.<br><br>Promethean is designed so product managers can write tests in natural language. They write evaluations like user stories, and they do not need to write Python.<br><br>The goal is to give product managers a more systematic way to evaluate LLM behavior. Data science teams still have a role, but product managers can run more of the day to day validation themselves. This can shorten the product development cycle, speed up iteration, and give teams more confidence when they ship LLM features.</td>
</tr>
<tr>
<td colspan="3">
<strong>Fable wrap-up</strong>, task 57, 
<code>powershell-meraki-link-pages</code>. 
The skill won 13 rules, the baseline won 5, and 7 were ties.
</td>
</tr>
<tr>
<td valign="top">Done. `pwsh -NoProfile -File test_meraki_pages.ps1` exits 0 with all 50 checks passing, and every rejection finding from the prior review is fixed and verified by adversarial loopback probes (probe scripts were scratch and have been removed). Protected files (`test_meraki_pages.ps1`, `docs/`) are untouched — git status shows only the four new module files.<br><br>**What was delivered**<br><br>- `MerakiPages.psm1` — sets StrictMode Latest, dot-sources the three implementation files, exports the six contract functions.<br>- `MerakiPages.Transport.ps1` — `New-MerakiContext` (trimmed BaseUri, default RetryLimit 3, default TrustedHosts `.meraki.com`/`.meraki.ca`/`.meraki.cn`/`.meraki.in`/`.gov-meraki.com`) and `Invoke-MerakiApi` on an `HttpClient` with `AllowAutoRedirect = $false`, so redirects are followed manually with a per-target trust decision.<br>- `MerakiPages.Paging.ps1` — `ConvertFrom-LinkHeader` (quoted and unquoted `rel`, ordinal hashtable) and `Get-MerakiPaged`, which follows the `rel=next` URL verbatim as an absolute `-Uri`.<br>- `MerakiPages.Inventory.ps1` — `Get-MerakiInventory` over `/organizations/{id}/networks` and `/devices`, and `ConvertTo-MerakiInventoryJson`, which hand-emits compact JSON in the pinned key order with `CompareOrdinal`/`StringComparer.Ordinal` sorting (no `ConvertTo-Json`, no `Format-*`).<br><br>**How each rejection finding was addressed** (each reproduced by an independent probe before cleanup)<br><br>1. *Key in error text*: all thrown messages pass through a redaction helper that does an ordinal `string.Replace` of the API key; the review's exact probe now yields `ErrorContainsApiKey:False` with `server echoed [REDACTED]`.<br>2. *Default-port authorities*: trust checks compare against the effective `host:port` built from `Uri.Host`/`Uri.Port` (which fills in scheme defaults) in addition to `Uri.Authority` and bare host — `example.test:443` against `https://example.test:443/next` (and against `https://example.test/next`) is now `Trusted:True`.<br>3. *Auth on initial absolute `-Uri`*: only `-Path` requests (built on the user-configured BaseUri) authenticate unconditionally. An absolute `-Uri` gets the bearer header only if its authority is trusted — a Meraki suffix, an injected authority, or the BaseUri's own authority (which is what lets same-shard pagination Link URLs keep auth). The untrusted-loopback probe now records an empty Authorization header.<br>4. *SleepAction output pollution*: the SleepAction invocation is assigned to `$null`; a 429→200 probe with an emitting SleepAction returns exactly one `PSCustomObject`.<br><br>**Official sources read** (research done before any code was written, via WebSearch then WebFetch; first-party Cisco/Meraki only)<br><br>- [Authentication — Meraki Dashboard API v1](https://developer.cisco.com/meraki/api-v1/authorization/) — standard `[REDACTED_SECRET] header; v0's `X-Cisco-Meraki-API-Key` deprecated; treat the key as a secret.<br>- [Pagination — Meraki Dashboard API v1](https://developer.cisco.com/meraki/api-v1/pagination/) — `perPage`/`startingAfter`/`endingBefore`, RFC 5988 Link header with first/prev/next/last, follow the next URL as given.<br>- [Rate Limit — Meraki Dashboard API v1](https://developer.cisco.com/meraki/api-v1/rate-limit/) — 10 req/s per org, 429 with `Retry-After` seconds and the `{"errors":[...]}` envelope.<br>- [How to Use the Cisco Meraki Dashboard API](https://documentation.meraki.com/Platform_Management/Dashboard_Administration/Operate_and_Maintain/How-Tos/How_to_Use_the_Cisco_Meraki_Dashboard_API) — 302 on GET, 307/308 on non-GET redirects; clients must follow redirects themselves because common HTTP libraries drop auth or substitute GET; regional hosts api.meraki.ca/.cn/.in and api.gov-meraki.com.<br>- [Get Organization Networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/) and [Get Organization Devices](https://developer.cisco.com/meraki/api-v1/get-organization-devices/) — paths, perPage ranges, and the id/name/productTypes and serial/name/model/networkId/productType response fields.<br><br>**One docs-vs-pinned-contract discrepancy to flag** (reporting rather than editing protected files, as instructed): `docs/contract.json` pins the networks `perPage` range as 3–100000, but my read of the current Get Organization Networks page reported 3–1000 (default 1000). This doesn't affect the module — `PerPage` is passed through verbatim and never validated client-side — but if you rely on large network page sizes, it's worth re-checking that operation page directly. No other conflicts: auth header, redirect codes, Link relations, 429/Retry-After semantics, and both operations' fields all match the pinned contract.</td>
<td valign="top">Implemented and verified the Meraki Dashboard API v1 PowerShell module.<br><br>`pwsh -NoProfile -File test_meraki_pages.ps1` passes with `OK (50 checks)`. I also ran separate loopback probes for the prior review issues; those passed, and the scratch probe file was removed. Protected files were not changed: `test_meraki_pages.ps1` and everything under `docs/` remain untouched. Git status shows only these new files:<br><br>- `MerakiPages.psm1`<br>- `MerakiPages.Transport.ps1`<br>- `MerakiPages.Paging.ps1`<br>- `MerakiPages.Inventory.ps1`<br><br>## Files added<br><br>- `MerakiPages.psm1`<br>  - Enables `Set-StrictMode -Version Latest`.<br>  - Dot-sources the three implementation files.<br>  - Exports the six required functions.<br><br>- `MerakiPages.Transport.ps1`<br>  - Implements `New-MerakiContext`.<br>  - Implements `Invoke-MerakiApi`.<br>  - Uses `HttpClient` with `AllowAutoRedirect = $false`.<br>  - Sends the v1 bearer Authorization header.<br>  - Handles redirects manually so Authorization is preserved only for trusted Meraki hosts, injected trusted authorities, or the configured base authority.<br>  - Handles 429 responses with `Retry-After` through the injected `SleepAction`.<br>  - Redacts the API key from thrown error messages.<br><br>- `MerakiPages.Paging.ps1`<br>  - Implements `ConvertFrom-LinkHeader`.<br>  - Parses both `rel=next` and `rel="next"` forms.<br>  - Implements `Get-MerakiPaged`.<br>  - Follows the `rel=next` URL exactly as returned, without rebuilding the query string.<br><br>- `MerakiPages.Inventory.ps1`<br>  - Implements `Get-MerakiInventory`.<br>  - Fetches organization networks and devices.<br>  - Implements `ConvertTo-MerakiInventoryJson`.<br>  - Produces compact, deterministic JSON with the pinned property order.<br>  - Sorts networks by `id`, devices by `serial`, and product types using ordinal string ordering.<br>  - Does not use `Format-*` in data<br><br>[...]</td>
<td valign="top">The Meraki PowerShell module is implemented, and the acceptance test passes. I ran `pwsh -NoProfile -File test_meraki_pages.ps1`, and it exited 0 with all 50 checks passing. I did not edit the protected files, including `test_meraki_pages.ps1` and everything under `docs/`. The only new files are the four module files.<br><br>Files added:<br><br>- `MerakiPages.psm1`<br>  - Sets `Set-StrictMode -Version Latest`.<br>  - Dot-sources the implementation files.<br>  - Exports the six functions required by the test contract.<br><br>- `MerakiPages.Transport.ps1`<br>  - Implements `New-MerakiContext`.<br>  - Implements `Invoke-MerakiApi`.<br>  - Uses `HttpClient` with automatic redirects disabled.<br>  - Sends the documented bearer token header.<br>  - Follows redirects manually.<br>  - Keeps the Authorization header only for trusted Meraki hosts, injected trusted authorities, or the configured base host.<br>  - Handles 429 responses by calling the injected `SleepAction` with the exact `Retry-After` value.<br>  - Throws on non-success responses with the HTTP status and documented error messages.<br>  - Redacts the API key from thrown error text.<br><br>- `MerakiPages.Paging.ps1`<br>  - Implements `ConvertFrom-LinkHeader`.<br>  - Handles both `rel=next` and `rel="next"` forms.<br>  - Uses ordinal string handling for the returned hashtable.<br>  - Implements `Get-MerakiPaged`.<br>  - Follows the `rel=next` URL exactly as returned by the API.<br><br>- `MerakiPages.Inventory.ps1`<br>  - Implements `Get-MerakiInventory`.<br>  - Fetches organization networks and devices.<br>  - Implements `ConvertTo-MerakiInventoryJson`.<br>  - Emits compact JSON with the pinned key order.<br>  - Sorts networks by `id`, devices by `serial`, and `productTypes` by ordinal order.<br>  - Does not use `ConvertTo-Json` or `Format-*` in the data path.<br><br>I also checked the specific failure cases from the pri<br><br>[...]</td>
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
<td valign="top">Your export likely failed because yesterday’s deploy changed the data schema that the export job expects.<br><br>A “schema mismatch” usually means the exporter expected one set of fields, types, or column names, but the data now has something different. Common causes include:<br><br>- A column was renamed, removed, or added<br>- A field type changed, such as `string` to `integer`, `date` to `timestamp`, or nullable to required<br>- The export template or saved query still references the old schema<br>- A downstream destination, such as a warehouse table or CSV mapping, has not been updated<br>- Cached metadata from before the deploy is still being used<br>- A migration ran partially or failed, leaving the app and database out of sync<br><br>To troubleshoot:<br><br>1. Check the deploy notes or migration diff from yesterday.<br>2. Compare the export’s expected schema with the current database/API schema.<br>3. Look for renamed, removed, or type-changed fields in the export logs.<br>4. Refresh or regenerate the export configuration if it uses cached metadata.<br>5. Update the destination table or mapping to match the new schema.<br>6. If the export depends on backward compatibility, restore the old field names or add a compatibility layer.<br><br>If this started immediately after the deploy, the most likely explanation is that the export job was not updated to match a schema change introduced in that release.</td>
<td valign="top">Your export likely failed because yesterday's deploy changed the shape of the data that the exporter writes, but the export schema was not updated at the same time.<br><br>A "schema mismatch" means the exporter produced data with fields or types that did not match what the destination expected. For example, the deploy may have added a new field, renamed a field, removed a field, or changed a value from a string to a number. When the destination checked the export against its saved schema, the check failed and the export stopped.<br><br>The most likely causes are:<br><br>- The deploy changed one or more export fields.<br>- The destination still expects the old schema.<br>- A migration or schema update did not run.<br>- The export job picked up mixed data from before and after the deploy.<br>- A cached schema was still in use after the deploy.<br><br>To debug it, check the export logs for the exact field name in the mismatch. Then compare the schema used by the exporter with the schema expected by the destination. If the deploy included a schema migration, confirm that the migration ran in the same environment where the export failed.<br><br>A safe fix is usually to update the destination schema, rerun the missing migration, or roll back the export field change until both sides use the same schema. If the export wrote partial output before failing, delete or overwrite the partial file before you rerun the job.</td>
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
