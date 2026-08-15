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

History items load a conversation from `evals/sources/` and append the
item prompt as the last user turn. Fable traces are rebuilt with
`uv run python evals/build_fable_histories.py`.

### Baseline

The same user messages are sent to the writer with a short system prompt:
write a clear, complete response, and return only the requested writing.
The writer does not see `SKILL.md`.

### Skill condition

The same user messages are sent again, to the same model, with `SKILL.md`
in the system prompt. The writer is told to follow those rules. It does
not see the baseline output.

### How it is judged

A judge compares the two outputs on each numbered rule in `SKILL.md`.
For each rule it sees the task prompt and two unlabeled texts, A and B.
The labels are shuffled so the judge does not know which text used the
skill. It returns `a`, `b`, or `tie` for that rule only.

An item is a skill win if the skill text wins more rules than the
baseline, a baseline win if the reverse is true, and a tie if the rule
counts are equal. The summary also totals those rule wins across items.

The default rewriter and judge are `gpt-5.5`. Override them with
`--model` and `--judge-model`.

## How to run

```
uv sync
uv run python evals/run_eval.py
uv run python evals/run_eval.py --category fable_coding
uv run python evals/run_eval.py --ids 66,67
uv run python evals/write_readme.py
```

Put `OPENAI_API_KEY` in a `.env` file at the repo root. Outputs land in
`evals/outputs/` and are gitignored. This README is updated from those
outputs by `write_readme.py`.

## Latest fable coding results

Category `fable_coding`, items `51`–`65`. The rewriter gets the full
trace and the longest wrap-up. The judge compares the baseline rewrite
to the skill rewrite on each writing rule.

| Metric | Result |
| --- | --- |
| Items | 15 |
| Skill wins / baseline wins / ties | 14 / 1 / 0 |
| Item win rate among decisive | 93% |
| Criterion skill / baseline / tie | 172 / 68 / 135 |
| Criterion win rate among decisive | 72% |
| Errors | 0 |
| Rewriter / judge | gpt-5.5 / gpt-5.5 |

Rules with the largest gap:

| Rule | Skill / baseline / tie | Skill win rate |
| --- | --- | --- |
| 2. No jargon. | 15 / 0 / 0 | 100% |
| 8. Write complete sentences. | 15 / 0 / 0 | 100% |
| 10. Organize a paragraph as a topic sentence and then support. | 15 / 0 / 0 | 100% |
| 12. Prefer long, explanatory sentences over short, punchy ones. | 14 / 1 / 0 | 93% |
| 19. You can use lists, but do not overuse them. | 14 / 1 / 0 | 93% |
| 1. Use simple, everyday words. | 13 / 2 / 0 | 87% |
| 17. Use straight quotes, not curly quotes. | 10 / 0 / 5 | 100% |
| 15. No dashes or middle dots. | 9 / 0 / 6 | 100% |

Rules where the baseline won more often:

| Rule | Skill / baseline / tie | Skill win rate |
| --- | --- | --- |
| 5. It's ok to use contractions. | 0 / 1 / 14 | 0% |
| 4. Stick to the same word; repetition is fine. | 6 / 9 / 0 | 40% |
| 25. Do not open with a count of things. | 2 / 5 / 8 | 29% |
| 11. Never write three or more clauses in one sentence, or three or more example sentences in a row. | 3 / 12 / 0 | 20% |
| 13. Be precise and unambiguous, and cut unnecessary clauses. | 3 / 12 / 0 | 20% |

## Fable examples

Each sample shows the raw wrap-up, the baseline-rewritten text, and the
skill-based rewritten text. Long texts are cut after about 900 characters.

### Item 51: `csharp-newrelic-synthetic-monitor`

Judge: skill_better=True (12-5-8).

Raw text:

```
Done — `dotnet test` passes 15/15, and the only changes are three new files under `src/`: `NerdGraphClient.cs`, `MonitorReconciler.cs`, and `Exceptions.cs` (all in `Acme.NewRelic.Synthetics`). Every protected file, `docs/`, and the starter `src/MonitorModels.cs` are byte-identical to the seed, and no scratch artifacts were left behind.

How the implementation addresses the outstanding review findings, alongside the pinned contract:

- **Transport** (`src/NerdGraphClient.cs`): POSTs exactly `{query, variables}` as `application/json` with the `API-Key` header; the key never touches the URL or body. HTTP 429 retries through the injected delay with 1s then 2s waits for at most three total attempts, then `NerdGraphHttpException(.Status)`; other non-2xx statuses surface immediately.
- **Key redaction** (finding: reflected-key leak): the raw response body is scrubbed of the API key at the trans

[...]
```

Baseline-rewritten:

```
Implemented the scripted API monitor reconciler and verified it with the acceptance suite.

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

[...]
```

Skill-based rewritten:

```
`dotnet test` passes with 15 passing tests and 0 failing tests.

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

[...]
```

### Item 54: `csharp-okta-systemlog-after`

Judge: skill_better=True (14-4-7).

Raw text:

```
Done. `dotnet test` passes 6/6, the workspace contains only the three new source files (`SystemLogModels.cs`, `SystemLogClient.cs`, `SystemLogExporter.cs`, all in namespace `OktaSyslog`), and every protected file — `SystemLogTests.cs`, `OktaSystemLog.csproj`, `.gitignore`, and everything under `docs/` — is untouched. The scratch copy of the OpenAPI spec I downloaded for research was deleted before finishing.

**Documentation conflict you should know about:** the current official System Log query guide states verbatim that "`since` and `after` are mutually exclusive and can't be specified simultaneously." The pinned contract disagrees — `docs/contract.json` (pagination.checkpoint) and the resume assertions in `SystemLogTests.cs:363-366` require a resumed sweep to send **both** `since` and `after`. I implemented the pinned behavior and left the protected files alone, as instructed; if this

[...]
```

Baseline-rewritten:

```
Implemented the Okta System Log exporter library.

Verification:
- `dotnet test` passes: 6 passed, 0 failed.
- Added only three source files:
  - `SystemLogModels.cs`
  - `SystemLogClient.cs`
  - `SystemLogExporter.cs`
- All new code is in namespace `OktaSyslog`.
- Protected files were not modified:
  - `SystemLogTests.cs`
  - `OktaSystemLog.csproj`
  - `.gitignore`
  - everything under `docs/`
- The temporary OpenAPI spec file downloaded for research was deleted.

Important documentation mismatch:
- The current Okta System Log query guide says: "`since` and `after` are mutually exclusive and can't be specified simultaneously."
- The pinned project contract disagrees. `docs/contract.json` and the resume assertions in `SystemLogTests.cs:363-366` require resumed sweeps to send both `since` and `after`.
- I implemented the pinned contract, as required, and left the protected files unchanged

[...]
```

Skill-based rewritten:

```
`dotnet test` passes 6 out of 6 tests.

I added three source files in the `OktaSyslog` namespace:

- `SystemLogModels.cs`
- `SystemLogClient.cs`
- `SystemLogExporter.cs`

I did not change the protected files:

- `SystemLogTests.cs`
- `OktaSystemLog.csproj`
- `.gitignore`
- Anything under `docs/`

I also deleted the temporary OpenAPI spec file that I downloaded for research.

## Documentation conflict

The current Okta System Log query guide says "`since` and `after` are mutually exclusive and can't be specified simultaneously."

The pinned contract in this repository requires different behavior. `docs/contract.json` and the resume assertions in `SystemLogTests.cs` require a resumed sweep to send both `since` and `after`.

I implemented the pinned contract and did not change the protected files. If this exporter is used against a live Okta org, the resume query may need to omit `since` wh

[...]
```

### Item 57: `powershell-meraki-link-pages`

Judge: skill_better=True (14-2-9).

Raw text:

```
Done. `pwsh -NoProfile -File test_meraki_pages.ps1` exits 0 with all 50 checks passing, and every rejection finding from the prior review is fixed and verified by adversarial loopback probes (probe scripts were scratch and have been removed). Protected files (`test_meraki_pages.ps1`, `docs/`) are untouched — git status shows only the four new module files.

**What was delivered**

- `MerakiPages.psm1` — sets StrictMode Latest, dot-sources the three implementation files, exports the six contract functions.
- `MerakiPages.Transport.ps1` — `New-MerakiContext` (trimmed BaseUri, default RetryLimit 3, default TrustedHosts `.meraki.com`/`.meraki.ca`/`.meraki.cn`/`.meraki.in`/`.gov-meraki.com`) and `Invoke-MerakiApi` on an `HttpClient` with `AllowAutoRedirect = $false`, so redirects are followed manually with a per-target trust decision.
- `MerakiPages.Paging.ps1` — `ConvertFrom-LinkHeader` (quo

[...]
```

Baseline-rewritten:

```
Implemented the Meraki Dashboard API v1 PowerShell module and verified it with the acceptance test.

`pwsh -NoProfile -File test_meraki_pages.ps1` passes with `OK (50 checks)`. I also ran temporary adversarial loopback probes for the prior review issues; they passed, and the probe file was removed. Protected files were not modified: `test_meraki_pages.ps1` and everything under `docs/` are unchanged. The only new files are the module files.

## Files added

- `MerakiPages.psm1`
  - Sets `Set-StrictMode -Version Latest`.
  - Dot-sources the implementation files.
  - Exports the required functions:
    - `New-MerakiContext`
    - `Invoke-MerakiApi`
    - `ConvertFrom-LinkHeader`
    - `Get-MerakiPaged`
    - `Get-MerakiInventory`
    - `ConvertTo-MerakiInventoryJson`

- `MerakiPages.Transport.ps1`
  - Implements `New-MerakiContext`.
  - Stores `BaseUri` without a trailing slash.
  - Default

[...]
```

Skill-based rewritten:

```
The Meraki PowerShell module is implemented, and the acceptance test passes. I ran `pwsh -NoProfile -File test_meraki_pages.ps1`, and it passed all 50 checks with exit code 0. I did not edit the protected files, which are `test_meraki_pages.ps1` and everything under `docs/`. The only new files are the four module files.

Summary:

- `MerakiPages.psm1`
  - Sets `Set-StrictMode -Version Latest`.
  - Dot-sources the three implementation files.
  - Exports the six required functions.

- `MerakiPages.Transport.ps1`
  - Implements `New-MerakiContext`.
  - Implements `Invoke-MerakiApi`.
  - Trims the trailing slash from `BaseUri`.
  - Sets the default `RetryLimit` to 3.
  - Sets the default trusted host suffixes to `.meraki.com`, `.meraki.ca`, `.meraki.cn`, `.meraki.in`, and `.gov-meraki.com`.
  - Uses `HttpClient` with `AllowAutoRedirect = $false`, so the module handles redirects itself.

- `M

[...]
```

## Latest items 66 and 67

These two prompts check the chat-context rule and the short-list rule.

| Metric | Result |
| --- | --- |
| Items | 2 |
| Skill wins / baseline wins / ties | 2 / 0 / 0 |
| Item win rate among decisive | 100% |
| Criterion skill / baseline / tie | 20 / 3 / 27 |
| Criterion win rate among decisive | 87% |
| Errors | 0 |
| Rewriter / judge | gpt-5.5 / gpt-5.5 |
