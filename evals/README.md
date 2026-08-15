# Plain-writing evals

These evals compare a baseline rewrite against a rewrite that is given
`SKILL.md`. A judge scores each pair on every numbered rule in the skill.

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

## Dataset

There are 67 items in `dataset.jsonl`.

- `01`–`40`: short prompts, public-domain excerpts, and LLM slop.
- `41`–`50`: long research and support-agent histories.
- `51`–`65`: long Claude Fable 5 coding-agent traces. The model sees the
  full trace and rewrites the longest wrap-up.
- `66`–`67`: chat context and lists-or-tables checks.

Fable traces are rebuilt with `uv run python evals/build_fable_histories.py`.

## Latest fable coding results

Category `fable_coding`, items `51`–`65`. The rewriter gets the full
trace and the longest wrap-up. The judge compares the baseline rewrite
to the skill rewrite on each writing rule.

| Metric | Result |
| --- | --- |
| Items | 15 |
| Skill wins / baseline wins / ties | 15 / 0 / 0 |
| Item win rate among decisive | 100% |
| Criterion skill / baseline / tie | 175 / 70 / 130 |
| Criterion win rate among decisive | 71% |
| Errors | 0 |
| Rewriter / judge | gpt-5.5 / gpt-5.5 |

Rules with the largest gap:

| Rule | Skill / baseline / tie | Skill win rate |
| --- | --- | --- |
| 8. Write complete sentences. | 15 / 0 / 0 | 100% |
| 12. Prefer long, explanatory sentences over short, punchy ones. | 15 / 0 / 0 | 100% |
| 19. If you are writing an essay, use lists and tables sparingly. If you are writing a brief, use lists and tables, but keep them short. | 15 / 0 / 0 | 100% |
| 10. Organize a paragraph as a topic sentence and then support. | 13 / 2 / 0 | 87% |
| 17. Use straight quotes, not curly quotes. | 11 / 1 / 3 | 92% |
| 15. No dashes or middle dots. | 10 / 0 / 5 | 100% |
| 16. Don't use colons to join clauses in ordinary prose. | 10 / 0 / 5 | 100% |
| 2. No jargon. | 11 / 2 / 2 | 85% |

Rules where the baseline won more often:

| Rule | Skill / baseline / tie | Skill win rate |
| --- | --- | --- |
| 21. No analogies or imagery. | 2 / 3 / 10 | 40% |
| 25. Do not open with a count of things. | 3 / 5 / 7 | 38% |
| 13. Be precise and unambiguous, and cut unnecessary clauses. | 6 / 9 / 0 | 40% |
| 11. Never write three or more clauses in one sentence, or three or more example sentences in a row. | 0 / 14 / 1 | 0% |

## Fable before and after

Each sample is the original longest wrap-up, the baseline rewrite, and
the rewrite with the skill. Long texts are cut after about 900 characters.

### Item 51: `csharp-newrelic-synthetic-monitor`

Judge: skill_better=True (11-7-7).

Original wrap-up:

```
Done — `dotnet test` passes 15/15, and the only changes are three new files under `src/`: `NerdGraphClient.cs`, `MonitorReconciler.cs`, and `Exceptions.cs` (all in `Acme.NewRelic.Synthetics`). Every protected file, `docs/`, and the starter `src/MonitorModels.cs` are byte-identical to the seed, and no scratch artifacts were left behind.

How the implementation addresses the outstanding review findings, alongside the pinned contract:

- **Transport** (`src/NerdGraphClient.cs`): POSTs exactly `{query, variables}` as `application/json` with the `API-Key` header; the key never touches the URL or body. HTTP 429 retries through the injected delay with 1s then 2s waits for at most three total attempts, then `NerdGraphHttpException(.Status)`; other non-2xx statuses surface immediately.
- **Key redaction** (finding: reflected-key leak): the raw response body is scrubbed of the API key at the trans

[...]
```

Baseline rewrite:

```
Implemented the scripted API monitor reconciler and verified it with the acceptance tests.

`dotnet test` passes:

- Failed: 0
- Passed: 15
- Total: 15

Changed files:

- `src/NerdGraphClient.cs`
- `src/MonitorReconciler.cs`
- `src/Exceptions.cs`

No protected files were changed. `docs/`, `SyntheticMonitorTests.cs`, `SyntheticMonitor.csproj`, `.gitignore`, and `src/MonitorModels.cs` are unchanged. No temporary files were left behind.

Implementation summary:

- `NerdGraphClient` sends NerdGraph requests as `POST` JSON bodies with exactly `query` and `variables`.
- Authentication uses the documented `API-Key` header.
- The API key is never placed in the URL or request body.
- HTTP 429 responses retry through the injected delay function with 1-second and 2-second delays, for three total attempts.
- Non-429 non-success HTTP responses fail immediately with `NerdGraphHttpException`.
- Respons

[...]
```

Rewrite with the skill:

```
`dotnet test` passes. The run passed all 15 tests.

The only changed files are new source files under `src/`:

- `src/NerdGraphClient.cs`
- `src/MonitorReconciler.cs`
- `src/Exceptions.cs`

All three files use the `Acme.NewRelic.Synthetics` namespace. I did not change `SyntheticMonitorTests.cs`, `SyntheticMonitor.csproj`, `.gitignore`, any file under `docs/`, or `src/MonitorModels.cs`. No temporary files were left behind.

Summary: I added a .NET 10 reconciler for New Relic scripted API synthetic monitors. The reconciler discovers existing monitors through NerdGraph entity search, creates missing monitors, updates existing monitors by GUID, preserves stored scripts when no new script is provided, and updates tags through the documented tagging mutation.

The transport code is in `src/NerdGraphClient.cs`. It sends one GraphQL document per request with a JSON body containing only `query` a

[...]
```

### Item 54: `csharp-okta-systemlog-after`

Judge: skill_better=True (9-7-9).

Original wrap-up:

```
Done. `dotnet test` passes 6/6, the workspace contains only the three new source files (`SystemLogModels.cs`, `SystemLogClient.cs`, `SystemLogExporter.cs`, all in namespace `OktaSyslog`), and every protected file — `SystemLogTests.cs`, `OktaSystemLog.csproj`, `.gitignore`, and everything under `docs/` — is untouched. The scratch copy of the OpenAPI spec I downloaded for research was deleted before finishing.

**Documentation conflict you should know about:** the current official System Log query guide states verbatim that "`since` and `after` are mutually exclusive and can't be specified simultaneously." The pinned contract disagrees — `docs/contract.json` (pagination.checkpoint) and the resume assertions in `SystemLogTests.cs:363-366` require a resumed sweep to send **both** `since` and `after`. I implemented the pinned behavior and left the protected files alone, as instructed; if this

[...]
```

Baseline rewrite:

```
Implemented the Okta System Log exporter library.

Verification:
- `dotnet test` passes: 6 passed, 0 failed.
- Added only these source files:
  - `SystemLogModels.cs`
  - `SystemLogClient.cs`
  - `SystemLogExporter.cs`
- All added code is in namespace `OktaSyslog`.
- Protected files were not modified:
  - `SystemLogTests.cs`
  - `OktaSystemLog.csproj`
  - `.gitignore`
  - everything under `docs/`
- The temporary OpenAPI spec file used during research was deleted before finishing.

Important documentation mismatch:
- The current Okta System Log query guide says: “`since` and `after` are mutually exclusive and can't be specified simultaneously.”
- The pinned project contract requires the opposite for resume behavior: `docs/contract.json` and the tests require resumed sweeps to send both `since` and `after`.
- I implemented the pinned test contract and did not modify protected files.
- If t

[...]
```

Rewrite with the skill:

```
`dotnet test` passes all 6 tests.

I added three source files in the `OktaSyslog` namespace:

- `SystemLogModels.cs`
- `SystemLogClient.cs`
- `SystemLogExporter.cs`

I did not modify the protected files:

- `SystemLogTests.cs`
- `OktaSystemLog.csproj`
- `.gitignore`
- Anything under `docs/`

I also deleted the temporary OpenAPI spec file that I downloaded for research.

Important documentation note: the current official Okta System Log query guide says "`since` and `after` are mutually exclusive and can't be specified simultaneously." The pinned contract in this repo requires different behavior. `docs/contract.json` and the resume assertions in `SystemLogTests.cs` require a resumed sweep to send both `since` and `after`. I followed the pinned contract because the ticket says the tests are the acceptance contract and the protected files must not be changed. If this exporter is later used

[...]
```

### Item 57: `powershell-meraki-link-pages`

Judge: skill_better=True (10-4-11).

Original wrap-up:

```
Done. `pwsh -NoProfile -File test_meraki_pages.ps1` exits 0 with all 50 checks passing, and every rejection finding from the prior review is fixed and verified by adversarial loopback probes (probe scripts were scratch and have been removed). Protected files (`test_meraki_pages.ps1`, `docs/`) are untouched — git status shows only the four new module files.

**What was delivered**

- `MerakiPages.psm1` — sets StrictMode Latest, dot-sources the three implementation files, exports the six contract functions.
- `MerakiPages.Transport.ps1` — `New-MerakiContext` (trimmed BaseUri, default RetryLimit 3, default TrustedHosts `.meraki.com`/`.meraki.ca`/`.meraki.cn`/`.meraki.in`/`.gov-meraki.com`) and `Invoke-MerakiApi` on an `HttpClient` with `AllowAutoRedirect = $false`, so redirects are followed manually with a per-target trust decision.
- `MerakiPages.Paging.ps1` — `ConvertFrom-LinkHeader` (quo

[...]
```

Baseline rewrite:

```
Implemented and verified the Meraki Dashboard API v1 PowerShell module.

`pwsh -NoProfile -File test_meraki_pages.ps1` now exits successfully with all 50 checks passing. The protected files were not changed: `test_meraki_pages.ps1` and everything under `docs/` remain untouched. Git status showed only four new module files.

## Files added

- `MerakiPages.psm1`
  - Enables `Set-StrictMode -Version Latest`.
  - Dot-sources the implementation files.
  - Exports the six required functions.

- `MerakiPages.Transport.ps1`
  - Implements `New-MerakiContext`.
  - Implements `Invoke-MerakiApi`.
  - Uses an `HttpClient` with `AllowAutoRedirect = $false`.
  - Handles redirects manually so the bearer token is preserved only for trusted targets.
  - Handles 429 responses with `Retry-After` and the injected `SleepAction`.
  - Redacts the API key from thrown errors.

- `MerakiPages.Paging.ps1`
  - Impl

[...]
```

Rewrite with the skill:

```
The Meraki PowerShell module is implemented, and the acceptance test passes. I ran `pwsh -NoProfile -File test_meraki_pages.ps1`, and it exited 0 with all 50 checks passing. I also ran separate loopback probes for the prior review findings, and each probe passed. I removed the scratch probe script after verification. The protected files, `test_meraki_pages.ps1` and everything under `docs/`, were not changed. Git status showed only four new module files.

Summary:
- Added `MerakiPages.psm1`.
- Added `MerakiPages.Transport.ps1`.
- Added `MerakiPages.Paging.ps1`.
- Added `MerakiPages.Inventory.ps1`.

`MerakiPages.psm1` sets `Set-StrictMode -Version Latest`, dot-sources the three implementation files, and exports the six contract functions.

`MerakiPages.Transport.ps1` contains `New-MerakiContext` and `Invoke-MerakiApi`. `New-MerakiContext` trims the trailing slash from `BaseUri`, defaults `

[...]
```

## Latest items 66 and 67

These two prompts check the chat-context rule and the lists-or-tables rule.

| Metric | Result |
| --- | --- |
| Items | 2 |
| Skill wins / baseline wins / ties | 2 / 0 / 0 |
| Item win rate among decisive | 100% |
| Criterion skill / baseline / tie | 21 / 3 / 26 |
| Criterion win rate among decisive | 88% |
| Errors | 0 |
| Rewriter / judge | gpt-5.5 / gpt-5.5 |
