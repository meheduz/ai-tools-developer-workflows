# Project 44 — AI Tools in Developers' Workflows

**Theme:** Technology, AI & Digital World
**Authors:** Mustari Ifthe (2023331050); Md. Meheduz Zaman (2023331064)
**Date:** 3 October 2026

## Abstract

Using the official Stack Overflow Developer Survey releases for 2023–2025, we describe current AI use, sentiment, trust, experience, roles and Bangladesh's position within the responding sample. Current use increased from 44.38% to 78.50%, while favorable sentiment decreased from 76.28% to 59.72%. Bangladesh's descriptive adoption rate exceeded the global rate in each year, although its valid samples were only 490, 324 and 194. Experience and adoption were associated within every year, with Cramér's V between 0.0843 and 0.1491. These findings describe self-selected respondents; they cannot establish population trends or causal effects.

## 1. Question, data and method

**Research question:** How has AI tool adoption and sentiment among developers changed from 2023 to 2025, and how does Bangladesh compare with the global sample?

We use public CSVs and schemas from the [official Stack Overflow survey archive](https://github.com/StackExchange/Survey/tree/main/packages/archive), not a mirror. One row is a respondent's record within one release. This is a voluntary annual online survey, not a panel following individuals. The notebook preserves `raw_df`, works on a copy, uses relative paths and fixes the sampling seed at 42. `data/manifest.json` records exact URLs, sizes, acquisition date and SHA-256 hashes.

| Year | Local rows × columns | Country entries for Bangladesh |
|---|---:|---:|
| 2023 | 89,184 × 84 | 490 |
| 2024 | 65,437 × 114 | 327 |
| 2025 | 49,191 × 172 | 220 |

The 2024 dimensions match the brief. The 2025 archive contains 172 more rows than the official profile total of 49,019. Bangladesh country counts also differ: the profiles report 325 in 2024 and 219 in 2025. We document these release differences and retain the actual file values. The 2025 file has 177 distinct reported countries; question count is not equivalent to CSV column count. See the [2024 profile](https://survey.stackoverflow.co/2024/developer-profile), [2025 profile](https://survey.stackoverflow.co/2025/developers) and [2025 survey overview](https://survey.stackoverflow.co/2025/).

Before analysis, a schema crosswalk checks each AI column's existence, source question and observed answer options. Four choices are essential:

- **Adoption:** affirmative `AISelect` answers count as current use, including all three frequency options in 2025. Plans to use AI count as noncurrent. This consistently reproduces the approximate 44%, 62% and 79% series; “using or planning” is a different denominator/definition.
- **Trust:** `AIBen` measures accuracy trust in 2023, while `AIAcc` measures benefits that year. Trust uses `AIAcc` in 2024–2025. Names alone would produce an incorrect comparison.
- **Experience:** 2023–2024 use professional coding years; 2025 uses broader professional work experience and requests a blank for zero. Bands are therefore interpreted within year. Textual “less than 1” and “more than 50” become 0.5 and 51; invalid fractions or values outside the declared 0–70 analysis range become missing.
- **Products:** separate 2023 search/developer products, combined 2024 products and 2025 LLM models remain separate. Semicolon selections become nullable indicators per question and year. `DevType` is a single main role in these schemas.

Missing sentinels and whitespace are normalized, without imputing zeros. No exact duplicate records or within-year duplicate IDs were found. All 203,812 source rows remain in the analysis copy; complete cases are selected separately for each chart or test. The quality assessment reports missingness for every source column. In 2025, 42 work-experience entries fail the declared range/fraction rule; this is an analysis choice, not proof that every extreme value is impossible.

## 2. Descriptive results

### Adoption and Bangladesh

| Year | Global valid n | Current users | Global adoption | Bangladesh valid n | Bangladesh adoption |
|---|---:|---:|---:|---:|---:|
| 2023 | 87,973 | 39,042 | 44.38% | 490 | 57.96% |
| 2024 | 60,907 | 37,662 | 61.84% | 324 | 71.91% |
| 2025 | 33,720 | 26,469 | 78.50% | 194 | 88.14% |

Current use increased by **34.12 percentage points** from 2023 to 2025 among valid answerers. The global denominator includes every valid AI-use answer, even when country is missing. Bangladesh additionally requires a reported country and is included in the global sample. The country comparison remains descriptive, with no small experience or role subdivisions. The 2025 Bangladesh Wilson interval is 82.84%–91.97%; it describes binomial uncertainty conditional on the responding sample and cannot correct self-selection.

### Sentiment and trust

| Year | Sentiment n | Favorable, all answers | Favorable without Indifferent (n) | Trust n | Trust / distrust |
|---|---:|---:|---:|---:|---:|
| 2023 | 61,501 | 76.28% | 91.35% (51,354) | 61,396 | 42.15% / 27.17% |
| 2024 | 45,873 | 71.97% | 88.49% (37,309) | 37,302 | 43.04% / 30.37% |
| 2025 | 33,467 | 59.72% | 72.45% (27,587) | 33,297 | 32.79% / 45.70% |

“Favorable” combines Favorable and Very favorable. Contrary to the supplied brief's neutral-option claim, **Indifferent and Unsure are observed in all three files**. We show complete category distributions and the sensitivity excluding Indifferent, while retaining Unsure. Both definitions show falling favorable shares. This does not prove identical survey presentation or routing. Reported trust is confidence in tool output, not measured accuracy; in 2025 distrust exceeds trust among item answerers.

### Experience, role, age and selections

Within-year adoption is higher among less experienced respondents. In 2024 it is 69.76% for 1–5 professional coding years (n=17,053) and 53.12% for 11+ (n=18,132). In 2025 the corresponding professional work groups are 83.07% (n=8,032) and 75.71% (n=16,185); the broader construct prevents an exact cross-year experience comparison. The notebook additionally shows age, main-role, experience distribution and sentiment/trust by experience.

The most selected primary developer product is GitHub Copilot in 2023, while ChatGPT leads the combined 2024 question and openAI GPT (chatbot models) leads the 2025 model question. These are different constructs. Tables report both selected counts and question-answerer percentages; stacked tool charts report composition of all mentions, including an Other segment. Multiple selections mean mention composition is not respondent prevalence. Every chart states its valid n and has an interpretation.

## 3. Statistical evidence

At α=0.05, the primary family comprises three annual chi-square tests and one 2025 Mann–Whitney comparison, with **Holm correction** across all four.

**Chi-square hypotheses:** H0: current AI use and experience band are independent within a year. H1: they are associated. Counts are categorical; each respondent contributes once. Unobserved bands are removed, and all expected counts exceed five.

| Year | Complete-case n | Cramér's V | χ² (df) | Minimum expected count | Holm-adjusted p |
|---|---:|---:|---:|---:|---:|
| 2023 | 66,136 | 0.1411 | 1,317.078 (3) | 769.12 | 1.16 × 10⁻²⁸⁴ |
| 2024 | 50,298 | 0.1491 | 1,118.125 (3) | 1,044.45 | 1.28 × 10⁻²⁴¹ |
| 2025 | 31,104 | 0.0843 | 221.293 (2) | 1,447.41 | 8.85 × 10⁻⁴⁹ |

We reject independence in every year. The association magnitudes are modest, despite exceptionally small p-values. The smaller 2025 V should not be interpreted as proof of a weakening population relationship, because experience wording and sample composition differ.

**Mann–Whitney hypotheses:** H0: 2025 professional work-experience distributions are equal for current users and nonusers. H1: they differ. Users have median 10 years (n=24,567), compared with 14 years for nonusers (n=6,537). The rank-biserial effect is **−0.1527**, oriented so a negative value means users tend to report fewer years. U=68,032,635 and Holm-adjusted p=2.09 × 10⁻⁸⁰. Normality, skewness and variance diagnostics are reported; normality and equal variance are not required for this test. Integer-year ties receive the asymptotic tie correction. Unequal distribution shapes prevent interpreting the result solely as a median test.

Removing the 70-year cap increases this test's sample to 31,122 and changes rank-biserial only to −0.1531. This sensitivity supports the qualitative result without establishing causation.

Exploratory Spearman correlations use one 2025 complete-case sample of 14,930, including the model question. Use versus sentiment has rho=0.1865; experience versus sentiment rho=0.0785; use versus experience rho=−0.0077 (adjusted p=0.346). This selected subset differs from the primary test sample, explaining why the two experience associations need not agree. These three exploratory comparisons have their own Holm correction.

## 4. Limitations, conclusion and next steps

Voluntary participation creates coverage and self-selection bias. Annual respondent pools, question wording, answer lists and routing change. Missing AI-use responses increase from 1.36% in 2023 to 31.45% in 2025; complete cases may select respondents with different behavior. Country samples are small and overlap the global sample. Experience boundaries are approximations, and 2025 work experience is a different construct. Product questions cannot form a common trend. Large n makes modest effects statistically detectable. None of these associations establishes that AI causes a change in experience, sentiment or productivity.

Agent-productivity questions added in 2025 apply to agent users; no general AI-user versus nonuser productivity analysis is made here. Any extension must restrict its claims to that selected agent sample. Respect data attribution and avoid respondent re-identification.

**Conclusion:** Among valid survey respondents, current AI use rose substantially while favorable sentiment and reported trust declined by 2025. Bangladesh respondents reported higher current-use rates each year, with insufficient evidence for a representative national conclusion. Less experienced respondents reported more adoption within each release, with modest association effects. Further work should examine missingness, consistent developer-status subpopulations, alternative experience bands, agent-only outcomes and locally collected Bangladesh evidence.

The notebook exports a 203,812 × 133 cleaned CSV, a 133-row dictionary, aggregate tables and 29 figures. All 28 code cells passed in a fresh IPython process and exported values were read back. A sandbox socket restriction prevented the Jupyter kernel integration check; locally use Restart Kernel and Run All before submission.

## References and attribution

- [Official 2023 survey](https://survey.stackoverflow.co/2023/) and [2024 survey](https://survey.stackoverflow.co/2024/).
- [2025 survey](https://survey.stackoverflow.co/2025/) and [2025 developer profile](https://survey.stackoverflow.co/2025/developers).
- [2024 developer profile](https://survey.stackoverflow.co/2024/developer-profile).
- [2025 survey press release](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/).
- [Diving into the results of the 2025 Developer Survey](https://stackoverflow.blog/2025/08/01/diving-into-the-results-of-the-2025-developer-survey/).
- [Verified official retrospective, 30 September 2026](https://stackoverflow.blog/2026/09/30/getting-ready-for-2026-results-a-look-back-on-developer-survey-findings/). This is a retrospective reference; no 2026 response data are used.
- [Requested retrospective URL](https://stackoverflow.blog/2026/10/01/a-look-back-before-we-look-forward-a-developer-survey-retrospective) was unavailable during the audit; the verified official page above is used instead.
- [Official archive and licence notice](https://github.com/StackExchange/Survey/tree/main/packages/archive).

**Attribution:** Stack Overflow Developer Survey, Stack Exchange Inc. Database: ODbL 1.0; individual contents: DbCL 1.0. Preserve attribution and apply ODbL share-alike terms when distributing adapted databases. See `DATA_LICENSE.md`. All numerical findings come from the recorded CSVs and notebook outputs, not mirrors or simulated data.
