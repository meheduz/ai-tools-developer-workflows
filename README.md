# AI Tools in Developers' Workflows

**Project 44 · Theme 8: Technology, AI & Digital World**

Analysis of the official Stack Overflow Developer Surveys for **2023, 2024 and 2025**. Current AI use among respondents with valid answers rose from **44.38% to 78.50%**, while favorable sentiment fell from **76.28% to 59.72%**. These are descriptions of voluntary survey respondents, not population estimates or causal effects.

## Authors

- Mustari Ifthe · 2023331050
- Md. Meheduz Zaman · 2023331064

## Repository layout

```text
ai-tools-developer-workflows/
├── analysis.ipynb          # Executed analysis, explanations, charts and tests
├── report.md               # Short research report
├── requirements.txt        # Pinned direct dependencies
├── download_data.py        # Official downloader with SHA-256 verification
├── audit_project.py        # Independent checks of saved results and exports
├── data/
│   ├── manifest.json        # Exact sources, download date, sizes and checksums
│   ├── raw/<year>/          # Official schemas and local public response files
│   └── processed/          # Generated cleaned CSV and dictionary
└── results/                # Aggregate tables, figures and computed metrics
```

Public response CSVs and processed respondent CSVs are ignored by Git. Official schemas, aggregate results and the executed notebook are retained. The notebook can regenerate the processed files.

## Setup and run

Open a terminal in the repository folder. From its parent folder, first run `cd ai-tools-developer-workflows`. The audited environment used **Python 3.14.5**.

```zsh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python download_data.py
python -m jupyter notebook analysis.ipynb
```

In Jupyter, select the environment's Python kernel and **Restart Kernel and Run All Cells**. Keep the notebook in the repository root: its paths are relative to that directory. The setup cell prints library versions. A fixed seed of 42 controls random sampling.

The downloader uses the [official Stack Overflow archive](https://github.com/StackExchange/Survey/tree/main/packages/archive). It verifies existing files and downloads only missing ones; failed downloads or checksum mismatches stop execution. The notebook invokes the same fallback. It never creates simulated responses. Because the upstream `main` branch can change, replacement files must match the recorded hashes or be reviewed as a new release.

If downloading fails, place **both** `survey_results_public.csv` and `survey_results_schema.csv` in each of `data/raw/2023/`, `data/raw/2024/` and `data/raw/2025/`. The official archive calls these files `results.csv` and `schema.csv`; the script saves the descriptive local names. See `data/manifest.json` for the exact source of each file.

After running the notebook, check the results independently:

```zsh
python audit_project.py
```

## Data and definitions

| Release | Local response-file shape | Valid AI-use answers | Current-use rate |
|---|---:|---:|---:|
| 2023 | 89,184 × 84 | 87,973 | 44.38% |
| 2024 | 65,437 × 114 | 60,907 | 61.84% |
| 2025 | 49,191 × 172 | 33,720 | 78.50% |

Sources: [2023 survey](https://survey.stackoverflow.co/2023/), [2024 survey](https://survey.stackoverflow.co/2024/), [2025 survey](https://survey.stackoverflow.co/2025/) and their official archive. The 2025 archive differs from the published profile total of 49,019; Bangladesh country counts in the archive are 327 (2024) and 220 (2025), versus 325 and 219 in the profiles. These differences are documented rather than removed to force a match. See the [2024 profile](https://survey.stackoverflow.co/2024/developer-profile) and [2025 profile](https://survey.stackoverflow.co/2025/developers).

“Current use” counts affirmative `AISelect` answers, including all three frequency categories in 2025. Planning-only answers are noncurrent; missing answers remain missing. Complete cases are selected separately for each analysis, and every chart and test reports its n.

The schema crosswalk exposes important differences: 2023 trust is `AIBen`, later trust is `AIAcc`; 2025 measures professional work experience rather than professional coding experience; product questions differ by year. `DevType` is a single main role. Genuine multi-select questions receive nullable indicators per question and year. `Indifferent` sentiment is observed in all three releases, contrary to the original brief's claim of a 2025-only neutral option.

## Validation status

All 28 code cells executed sequentially in a fresh IPython process, with figures and rich outputs saved. Independent checks recompute adoption, sentiment, tool counts, chi-square statistics and the Mann–Whitney comparison from raw files, and check exported indicators and missingness.

A socket restriction in the audit environment prevented launching a Jupyter kernel. The fresh-process run checks computation; **Restart Kernel and Run All** in your local Jupyter remains the final kernel integration check.

## Licence and responsible use

**Data source and attribution:** Stack Overflow Developer Survey 2023, 2024 and 2025, published by **Stack Exchange Inc. / Stack Overflow**.

The [publisher's official archive and licence notice](https://github.com/StackExchange/Survey/tree/main/packages/archive) specifies the following terms, including for the 2023 release:

- **Database:** [Open Database License (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
- **Individual contents:** [Database Contents License (DbCL) 1.0](https://opendatacommons.org/licenses/dbcl/1-0/).

Suggested attribution:

> Contains information from the Stack Overflow Developer Survey, Stack Exchange Inc., made available under ODbL 1.0; individual contents under DbCL 1.0.

The raw CSVs retain their original values. The generated `data/processed/cleaned_survey.csv` is an adapted database: it standardizes missing values, harmonizes selected variables, validates experience values and adds indicators. Preserve attribution and notices, and follow the applicable ODbL share-alike requirements when redistributing adapted databases. Exact sources and transformations are documented in `data/manifest.json` and `analysis.ipynb`.

These terms apply to the survey data; this notice does not assign a software licence to the project's code.

Only official sources are used; no Kaggle data or 2026 survey results are included. Country comparisons are descriptive, Bangladesh is not subdivided into small cells, and no general AI-to-productivity causal claim is made. The optional predictive baseline is omitted because instructor approval has not been supplied.
