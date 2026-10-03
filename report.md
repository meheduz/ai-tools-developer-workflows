# AI Tools in Developers’ Workflows

## Evidence from the Stack Overflow Developer Surveys, 2023–2025

| Project information | Details |
|---|---|
| Project | 44 — Data Science Lab |
| Theme | Technology, AI & Digital World |
| Authors | Mustari Ifthe (2023331050); Md. Meheduz Zaman (2023331064) |
| Date | 3 October 2026 |
| Data publisher | Stack Overflow / Stack Exchange Inc. |

## Abstract

This study examines AI tool adoption, sentiment and trust in 203,812 records from the official Stack Overflow Developer Surveys for 2023–2025. Current use increased from 44.38% to 78.50%, while favorable sentiment decreased from 76.28% to 59.72%. Bangladesh respondents reported higher adoption each year, with valid samples of 490, 324 and 194. Experience and adoption were associated within each release, with Cramér’s V ranging from 0.0843 to 0.1491. The findings describe voluntary respondents; question changes, missing responses and small country samples limit generalization and causal interpretation.

## 1. Introduction and Research Objective

AI tool adoption, favorable sentiment and trust measure different aspects of developers’ workflows. This study examines each separately, alongside variation by experience, role and country.

> **Research question:** How have current AI use and sentiment among Stack Overflow Developer Survey respondents differed from 2023 to 2025, and how does Bangladesh compare with the global sample?

We compare current use, sentiment and trust across releases, then examine how use varies with experience, role and country. The analysis keeps track of question changes so that differences in measurement are not mistaken for changes in behavior.

## 2. Data and Methodology

### 2.1 Data Sources and Study Population

Public response files and schemas come from the [official survey archive](https://github.com/StackExchange/Survey/tree/main/packages/archive). Each row represents one voluntary respondent’s annual record; individuals cannot be tracked across releases. Exact URLs, sizes and SHA-256 checksums are recorded in `data/manifest.json`.

**Table 1. Dimensions of the analyzed response files**

| Release | Respondents | Source columns | Bangladesh country responses |
|---|---:|---:|---:|
| 2023 | 89,184 | 84 | 490 |
| 2024 | 65,437 | 114 | 327 |
| 2025 | 49,191 | 172 | 220 |

The 2025 archive exceeds the profile total of 49,019 by 172 records. Bangladesh counts also differ from the profile’s 325/219 for 2024/2025. Archive values are retained and discrepancies disclosed. The 2025 file has 177 reported countries; expanded CSV columns differ from the publisher’s 62 questions. [2024 profile](https://survey.stackoverflow.co/2024/developer-profile); [2025 profile](https://survey.stackoverflow.co/2025/developers); [2025 overview](https://survey.stackoverflow.co/2025/).

### 2.2 Variable Definitions and Harmonization

We read the three schemas before selecting variables. The crosswalk records each source question, whether its column exists and which answer categories appear in the files.

- **Current use:** Affirmative `AISelect` answers, including all 2025 frequencies, count as current use. Plans count as noncurrent; missing answers remain missing.
- **Sentiment:** Favorable combines Favorable and Very favorable. Full distributions retain Indifferent and Unsure; sensitivity excludes Indifferent only.
- **Favorable indicator:** `favorable_sentiment` records those two favorable categories as 1 and other valid responses as 0, including Indifferent and Unsure. Zero means not classified as favorable, rather than unfavorable. Unanswered sentiment remains missing; the valid denominator is unchanged.
- **Trust:** Use `AIBen` in 2023 and `AIAcc` in 2024–2025. The 2023 `AIAcc` question measures anticipated benefits.
- **Experience:** Use professional coding years (`YearsCodePro`) in 2023–2024 and broader work experience (`WorkExp`) in 2025. Bands are under one, 1–5, 6–10 and 11+ years, interpreted within release. The 2025 blank-zero instruction prevents distinguishing zero from nonresponse.
- **Roles and selections:** `DevType` is one main role. Semicolon selections receive question/year-specific indicators; skipped questions remain missing.

Product questions remain separate: 2023 search/development products, 2024 combined products and 2025 LLM models cannot form a common product trend.

### 2.3 Data Quality and Analysis Strategy

We trimmed category labels and converted blank strings and missing-value labels to missing values. Unanswered questions were not filled with zero. No exact duplicates or duplicate IDs within a release were found. All records were retained; each analysis selects its own complete cases. Missingness is reported for every source column.

Experience phrases below one/above 50 years become 0.5/51. Invalid fractions and values outside the declared 0–70 range are excluded from experience analyses, flagging 42 entries in 2025. Sensitivity assesses this analysis rule’s upper cap.

Every result reports the number of respondents included. Tests use α = 0.05, with effect sizes guiding the interpretation. Holm correction covers three annual chi-square tests and one 2025 Mann–Whitney comparison; three exploratory Spearman comparisons form a separate corrected family.

## 3. Results

### 3.1 Current AI Use and Bangladesh

**Table 2. Current AI use among respondents with valid answers**

| Release | Global valid n | Global current users | Global use | Bangladesh valid n | Bangladesh use |
|---|---:|---:|---:|---:|---:|
| 2023 | 87,973 | 39,042 | 44.38% | 490 | 57.96% |
| 2024 | 60,907 | 37,662 | 61.84% | 324 | 71.91% |
| 2025 | 33,720 | 26,469 | 78.50% | 194 | 88.14% |

Current use increased by **34.12 percentage points**. Global includes all valid AI-use answers; Bangladesh additionally requires country. Bangladesh is included globally, so the series overlap.

Current use among Bangladesh respondents exceeded the global sample rate each year. Its 2025 model-based 95% Wilson interval is 82.84%–91.97%, assuming independent-binomial responses without correcting participation bias. Country comparisons remain descriptive, without small Bangladesh subgroups. Annual Global Wilson intervals are also available in the notebook and `results/adoption_summary.csv`.

### 3.2 Sentiment and Trust

**Table 3. Favorable sentiment and reported trust in AI output**

| Release | Sentiment n | Favorable, all valid answers | Favorable excluding Indifferent (n) | Trust n | Trust / distrust |
|---|---:|---:|---:|---:|---:|
| 2023 | 61,501 | 76.28% | 91.35% (51,354) | 61,396 | 42.15% / 27.17% |
| 2024 | 45,873 | 71.97% | 88.49% (37,309) | 37,302 | 43.04% / 30.37% |
| 2025 | 33,467 | 59.72% | 72.45% (27,587) | 33,297 | 32.79% / 45.70% |

Favorable sentiment declined under both definitions. **Indifferent and Unsure occur in all three files**, so introducing Indifferent in 2025 cannot explain the decline. Observed labels do not establish identical routing or presentation.

Trust combines Somewhat/Highly trust; distrust combines the negative categories. Distrust exceeded trust in 2025. This measures confidence in output, not objective accuracy. Adoption, sentiment and trust have different respondent denominators.

### 3.3 Experience, Roles and Selected Products

Less experienced groups reported higher adoption within each release. In 2024, use was 69.76% for 1–5 coding years (n = 17,053) versus 53.12% for 11+ (n = 18,132). The 2025 work-experience groups reported 83.07% (n = 8,032) and 75.71% (n = 16,185); changed wording limits cross-year interpretation.

Among the ten largest 2025 roles, front-end developers reported 86.86% use (n = 1,484) and embedded developers 65.16% (n = 1,016). These descriptions do not isolate role effects. The notebook also examines age and sentiment/trust by experience.

GitHub Copilot led the 2023 development-product question at 85.23% (22,078/25,904), ChatGPT the combined 2024 question at 85.31% (37,923/44,453), and “openAI GPT (chatbot models)” the 2025 question at 82.45% (13,424/16,281). These percentages use respondent denominators; tool stacks show mention composition, including Other selections.

### 3.4 Statistical Associations

**AI use and experience band.** H₀: independence within release; H₁: association. Pearson’s chi-square uses categorical counts, with one contribution per respondent and unobserved bands removed. Respondent independence is assumed; every expected count exceeds five.

**Table 4. Annual chi-square tests, with effect sizes and Holm correction**

| Release | Complete-case n | Cramér’s V | χ² (df) | Minimum expected count | Adjusted p |
|---|---:|---:|---:|---:|---:|
| 2023 | 66,136 | 0.1411 | 1,317.078 (3) | 769.12 | 1.16 × 10⁻²⁸⁴ |
| 2024 | 50,298 | 0.1491 | 1,118.125 (3) | 1,044.45 | 1.28 × 10⁻²⁴¹ |
| 2025 | 31,104 | 0.0843 | 221.293 (2) | 1,447.41 | 8.85 × 10⁻⁴⁹ |

Independence is rejected each year; the numerical V values quantify the associations without assigning universal magnitude labels. Statistical significance alone does not establish practical importance. Changed wording and samples prevent interpreting the smaller 2025 V as a weakening population relationship.

**Work experience among users and nonusers.** H₀ states that their 2025 work-experience distributions are equal; H₁ states that they differ. The Mann–Whitney comparison yields **rank-biserial = −0.1527**, U = 68,032,635 and adjusted p = 2.09 × 10⁻⁸⁰. Users report a median of 10 years (IQR 5–20; n = 24,567), compared with 14 years among nonusers (IQR 7–25; n = 6,537). The negative effect indicates that users tend to report fewer years.

Normality, skewness and variance diagnostics are reported. The rank test requires neither normality nor equal variance, accounts for ties, and supports a rank/distribution interpretation. Removing the cap gives n = 31,122 and rank-biserial = −0.1531, preserving the substantive result.

**Exploratory correlations.** Spearman’s rank method describes monotonic associations involving ordinal sentiment, skewed/discrete experience and discrete selection counts. It uses one 2025 complete-case sample of 14,930 that also answered the model question. Use–sentiment correlation is positive (ρ = 0.1865), and experience–sentiment correlation is positive and close to zero (ρ = 0.0785). Use–experience correlation is near-zero negative (ρ = −0.0077; adjusted p = 0.346). Selection into this smaller sample limits comparison with the primary experience tests. None of these associations identifies a causal effect.

### 3.5 Focused Robustness Checks

**Table 5. Disjoint geographic comparison: current use (valid n; 95% Wilson interval)**

| Release | Bangladesh | Rest of World |
|---|---:|---:|
| 2023 | 57.96% (490; 53.54–62.25%) | 44.30% (87,483; 43.97–44.63%) |
| 2024 | 71.91% (324; 66.79–76.53%) | 61.03% (58,119; 60.63–61.43%) |
| 2025 | 88.14% (194; 82.84–91.97%) | 78.44% (33,526; 78.00–78.88%) |

The higher Bangladesh estimate persists in all releases. Rest of World excludes Bangladesh and requires country. In 2024, this also excludes 2,464 valid AI answers with missing country; its difference from the required Global estimate is therefore not solely due to removing Bangladesh.

**Experience bands (2025):** Main bands (1–5, 6–10, 11+): 83.07% → 81.92% → 75.71%; V=0.0843; Alternative bands (1–4, 5–9, 10+): 83.28% → 82.14% → 76.36%; V=0.0772. Both use n=31,104; the descending direction is **STABLE**, while exact rates and V vary. The alternative assigns 5 to the middle group and 10 to the highest; it approximates the [publisher’s overlapping career labels](https://survey.stackoverflow.co/2025/ai), not an undocumented endpoint convention.

**Complete cases:** From 49,191 records, 15,076 answered all four correlation source questions and 14,930 have valid derived values. Included versus incomplete records differ on observed characteristics: age 18–24 is 12.36% versus 21.49%; current use among valid AI answers is 96.85% versus 63.91% (n=14,930/18,790). This supports a conditional correlation interpretation; it does not identify the missingness mechanism. No new country test or correlation sensitivity family is added.

## 4. Discussion and Limitations

Increasing adoption coincided with declining favorable sentiment and lower trust by 2025. These sample-level patterns do not establish why attitudes changed or how they influenced individual behavior.

The banding check tests a **REDUCIBLE** analysis choice. Country overlap, complete-case selection and changing questions are **PARTIALLY REDUCIBLE**: diagnostics expose their effects without eliminating selection or construct differences. Self-selection and the repeated cross-sectional design are **INTRINSIC** limitations. Six limitations remain:

1. **Self-selection and coverage:** Recruitment through Stack Overflow channels and voluntary participation limit representation of the broader developer population, including Bangladesh. Increasing n does not remove this selection mechanism; no population weights are invented. [2024 methodology](https://survey.stackoverflow.co/2024/methodology); [2025 methodology](https://survey.stackoverflow.co/2025/methodology).
2. **Changing samples and instruments:** Annual respondents, question wording, available choices and routing differ; archive/profile discrepancies add uncertainty about release comparability.
3. **Missing responses:** AI-use missingness rises from 1.36% in 2023 to 31.45% in 2025. Complete cases may differ systematically from other respondents.
4. **Measurement choices:** Experience phrases are approximate, the upper range is analyst-defined, and professional coding/work experience and product/model questions measure different constructs.
5. **Country sample size:** Bangladesh’s small samples and overlap with the global series constrain country comparisons. Binomial intervals cannot remove participation bias.
6. **Association and selection:** Large samples can detect limited differences. Effect sizes reduce overinterpretation of significance, but practical importance still requires context. The study supports no causal or general productivity claim. Nonmissing 2025 agent-impact answers do not by themselves establish agent use; any future agent-user productivity analysis needs a verified agent-use restriction and routing review.

## 5. Conclusion and Future Work

Current AI use rose substantially among valid survey respondents between 2023 and 2025, while favorable sentiment declined and trust was lower in 2025. Bangladesh respondents reported higher current use in each release, with insufficient evidence for a representative national estimate. Within-year experience associations were statistically detectable, with Cramér’s V of 0.1411, 0.1491 and 0.0843. The robustness checks preserve the country direction and descending 2025 experience pattern, while exposing selection into the correlation subset.

Further research could extend the observed missingness profiles, examine consistent developer-status subpopulations and alternative experience definitions in other releases, and study agent-only productivity or locally collected evidence from Bangladesh. These extensions could clarify the patterns while retaining appropriate limits on generalization.

## Reproducibility and Data Attribution

The companion notebook follows Sections 0–16 of the lab handbook, exporting a 203,812 × 134 dataset, complete dictionary and 29 figures. It retains all 63 tool/model indicators, 49 main-role indicators and five response-status flags, with a feature-family inventory and 15 computational checks. The revised notebook executed in a fresh Jupyter kernel. It preserves the raw frame, fixes seed 42 and verifies exports by readback. Setup and execution-check details appear in [README.md](README.md).

**Attribution:** Stack Overflow Developer Survey, Stack Exchange Inc. The database is released under ODbL 1.0 and individual contents under DbCL 1.0. Preserve attribution and apply the relevant share-alike terms when distributing adapted databases. See [DATA_LICENSE.md](DATA_LICENSE.md) and the [publisher’s archive notice](https://github.com/StackExchange/Survey/tree/main/packages/archive). All numerical findings derive from the recorded official CSVs.

## References

1. Stack Overflow. [Developer Survey 2023](https://survey.stackoverflow.co/2023/).
2. Stack Overflow. [Developer Survey 2024](https://survey.stackoverflow.co/2024/) and [Developer Profile](https://survey.stackoverflow.co/2024/developer-profile).
3. Stack Overflow. [Developer Survey 2025](https://survey.stackoverflow.co/2025/) and [Developer Profile](https://survey.stackoverflow.co/2025/developers).
4. Stack Overflow. [2025 Developer Survey press release](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/).
5. Stack Overflow. [Diving into the Results of the 2025 Developer Survey](https://stackoverflow.blog/2025/08/01/diving-into-the-results-of-the-2025-developer-survey/).
6. Stack Overflow. [Official Survey Archive and Licence Notice](https://github.com/StackExchange/Survey/tree/main/packages/archive).
7. Stack Overflow. [Developer Survey Retrospective, 30 September 2026](https://stackoverflow.blog/2026/09/30/getting-ready-for-2026-results-a-look-back-on-developer-survey-findings/). Used as historical context; no 2026 response data are included.

**Reference availability note:** The originally supplied [1 October 2026 retrospective URL](https://stackoverflow.blog/2026/10/01/a-look-back-before-we-look-forward-a-developer-survey-retrospective) was unavailable during source verification. Reference 7 provides the verified official retrospective.
