# Project audit — 3 October 2026

**Project:** AI Tools in Developers' Workflows · Project 44
**Scope:** source files, notebook execution, cleaning, charts, statistical methods, exports, report, reproducibility and GitHub packaging.

## Result

The corrected analysis passes sequential execution in a fresh IPython process and independent checks against the raw CSVs. The notebook, report and README now agree. Local Jupyter kernel integration remains a manual check because this audit environment forbids opening the sockets required by a kernel. No new internet download or clean-environment installation was needed; those network-dependent paths were not exercised here.

## Issues found and corrected

| Issue | Correction |
|---|---|
| Report claimed dependencies/tests were unavailable and described outdated methods | Replaced with computed results, actual tests, assumptions, corrected p-values and effect sizes |
| Role question incorrectly described as multi-select | Verified `DevType` is one main role in all three schemas; confirmed no semicolon role responses |
| Tool summaries mixed releases/questions | Kept four question/year blocks separate; report percentages use each question's actual answerer denominator |
| A skipped product question could become zero after combining questions | Nullable indicators are generated per question and year; skipped/out-of-year selections remain missing |
| Adoption chart n was a user count rather than denominator; country restriction changed global rate | Global uses every valid AI-use answer; labels show valid n; Bangladesh additionally requires country |
| Professional work and professional coding years were treated as identical | Retained source meaning and restricted experience interpretation to within-year comparisons |
| Neutral-option claim contradicted actual files | Documented Indifferent and Unsure in all releases; showed full distributions and sensitivity excluding Indifferent |
| Trust column names change meaning | Explicit 2023 `AIBen` versus 2024–2025 `AIAcc` mapping, with observed-value validation |
| Inferential correction/diagnostics were incomplete | Holm correction covers all four primary tests; expected counts, group distributions, normality and variance diagnostics are reported |
| Correlations pooled incompatible measures and samples | 2025-only heatmap uses one complete-case sample; three exploratory correlations have separate Holm correction |
| Export omitted engineered indicators and lacked a complete dictionary | Export includes all question/year tool and main-role flags; dictionary describes every exported column |
| Downloads lacked exact provenance and integrity checking | Added six-file manifest and official downloader with SHA-256 verification and stop-on-failure behavior |
| Setup/package versions and generated-file handling were incomplete | Pinned tested direct dependencies; documented correct working folder; ignored caches, partial downloads and large respondent files |
| Requested retrospective reference was unavailable | Retained the requested link with an unavailable note and added a verified official retrospective link |

## Data verified

| Year | Raw shape | Distinct reported countries | Bangladesh country n | Valid global AI-use n | Current-use rate |
|---|---:|---:|---:|---:|---:|
| 2023 | 89,184 × 84 | 185 | 490 | 87,973 | 44.38% |
| 2024 | 65,437 × 114 | 185 | 327 | 60,907 | 61.84% |
| 2025 | 49,191 × 172 | 177 | 220 | 33,720 | 78.50% |

The 2025 archive does not match the official profile total of 49,019, and archive Bangladesh counts differ from the profile's 325/219. These discrepancies are retained and disclosed. The six source hashes and byte sizes match `data/manifest.json`. No duplicate records, missing IDs or duplicate IDs within a year were found. Raw files remain unchanged; a raw-frame fingerprint is checked during execution. No 2026 survey responses or mirror data are used.

## Execution and independent validation

- **28 of 28 code cells passed**, sequentially in a fresh process without prior analysis variables.
- **29 figures are embedded** in the saved notebook and exported to `results/`; four representative figures were visually inspected for labels, denominators and legibility.
- **48 rendered Markdown outputs** provide chart and test interpretations, alongside explanatory Markdown cells.
- The source-column missingness report was independently recomputed for every year and column.
- Raw-data recomputation reproduces adoption, Bangladesh counts, sentiment, trust mapping, tool selection counts and all four primary tests.
- Every exported tool indicator was checked against source token membership. Every main-role flag was also checked. Skipped questions and out-of-year tool fields retain missing values.
- The cleaned file is **203,812 × 133**; the dictionary has **133 rows**, in matching column order. Both are read back and checked. No universal complete-case deletion is applied.
- `python -m pip check` reports **No broken requirements found** in the existing environment. This does not constitute a new installation on another machine.
- Activating `.venv` selects the Python executable inside the renamed repository; `python -m jupyter --version` succeeds. Relative documentation links and Git exclusions pass checks; the largest repository candidate file is the approximately 1.9 MB notebook.
- `python audit_project.py` provides reusable independent checks; it reads files without downloading or changing data.

### Statistical results

| Test | n | Effect | Statistic | Holm-adjusted p |
|---|---:|---:|---:|---:|
| AI use × experience, 2023 | 66,136 | V=0.1411 | χ²=1,317.078; df=3 | 1.16 × 10⁻²⁸⁴ |
| AI use × experience, 2024 | 50,298 | V=0.1491 | χ²=1,118.125; df=3 | 1.28 × 10⁻²⁴¹ |
| AI use × experience, 2025 | 31,104 | V=0.0843 | χ²=221.293; df=2 | 8.85 × 10⁻⁴⁹ |
| 2025 user/nonuser experience | 31,104 | Rank-biserial=−0.1527 | U=68,032,635 | 2.09 × 10⁻⁸⁰ |

All chi-square expected counts exceed five. Mann–Whitney uses the asymptotic tie correction. The 2025 medians are 10 years (users, n=24,567) and 14 (nonusers, n=6,537). Diagnostic p-values can underflow to zero in stored numerical output; the notebook explains this numerical limit. Sensitivity without the 70-year cap gives rank-biserial −0.1531, n=31,122. Effects describe association, not causation.

## Submission coverage

| Area | Evidence |
|---|---|
| Title and problem | Authors/IDs, dataset links, date, computed abstract, main-goal quote, eight questions including two testable questions |
| Dataset and collection | Publisher, voluntary method, release period, unit, licence, clarification box, saved raw files and official fallback |
| Setup and inspection | One import cell, optional install, versions, shape/head/tail/sample/dtypes/info/describe, key dictionary and answered checkpoint |
| Quality and cleaning | Full missingness report, duplicate/ID checks, quality interpretation, nine numbered cleaning steps, range validation and per-analysis row counts |
| Features | Nine documented features/feature families with formula, reason and limitation |
| EDA | 29 charts, 100% stacked adoption/tools/sentiment views, age/role/country comparisons and seven grouped tables |
| Correlation and tests | One Spearman heatmap, three interpreted pairs, chi-square and Mann–Whitney with hypotheses, α, assumptions, n, effects and conclusions |
| Communication | Seven computed findings, more than five limitations, ethics, direct conclusion and short report (approximately 1,700 words) |
| Exports and reuse | Two read-back-verified CSVs; reusable inspection helper applied to raw and cleaned DataFrames |
| Summary and extensions | Stage summary, key-lesson box and seven realistic next steps |
| Optional model | Omitted; instructor approval has not been supplied |

The notebook presents the analysis itself; this coverage review is kept in this audit document.

## GitHub state

At the audit snapshot, the repository folder was `ai-tools-developer-workflows/` on branch `main`, with no configured remote, commit or push. Staged files and audit edits were available for review. Raw public response CSVs, processed respondent CSVs, `.venv/`, caches and partial downloads are ignored. Small schemas, manifest, downloader, executed notebook, aggregate figures/tables and documentation are suitable repository deliverables.

## Manual checks before submission or publishing

1. In the local environment, run **Restart Kernel and Run All** from the repository root. This is the remaining Jupyter kernel integration check.
2. Review the schema crosswalk, especially 2023 trust, single-role wording, the broader 2025 experience question and blank-zero instruction.
3. Explain the actual file/profile discrepancies without altering the released data to match headline totals.
4. Confirm the adoption definition excludes plans; explain the Indifferent mismatch and both sentiment denominators.
5. Distinguish tool mention composition from respondent percentages, and avoid comparing product and LLM questions as one trend.
6. Confirm spelling of authors/IDs, the desired GitHub remote and attribution/ODbL notices before publishing. The Markdown report's final page count depends on the submission renderer.
