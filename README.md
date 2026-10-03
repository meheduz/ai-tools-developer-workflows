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
├── download_data.py        # Official downloader with size and SHA-256 verification
├── audit_project.py        # Independent checks of saved results and exports
├── prepare_kaggle.py       # Builds the Kaggle dataset and notebook upload folders
├── kaggle/bootstrap.py     # Connects Kaggle inputs to relative project paths
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

For a fresh kernel execution from the terminal:

```zsh
python -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb --ExecutePreprocessor.timeout=900
python audit_project.py
```

The downloader uses the [official Stack Overflow archive](https://github.com/StackExchange/Survey/tree/main/packages/archive). It verifies recorded byte sizes and SHA-256 hashes for existing files and downloads only missing ones; failed downloads or integrity mismatches stop execution. The notebook invokes the same fallback and shows its acquisition code. It never creates simulated responses. Because the upstream `main` branch can change, replacement files must match the recorded release or be reviewed as a new release.

If downloading fails, place **both** `survey_results_public.csv` and `survey_results_schema.csv` in each of `data/raw/2023/`, `data/raw/2024/` and `data/raw/2025/`. The official archive calls these files `results.csv` and `schema.csv`; the script saves the descriptive local names. See `data/manifest.json` for the exact source of each file.

After running the notebook, check the results independently:

```zsh
python audit_project.py
```

## Run on Kaggle

Uploaded under **mdmeheduzzaman**, with private visibility:

- [Kaggle notebook](https://www.kaggle.com/code/mdmeheduzzaman/ai-tools-in-developers-workflows)
- [Kaggle dataset and project files](https://www.kaggle.com/datasets/mdmeheduzzaman/ai-tools-developer-workflows-2023-2025)

The Kaggle notebook uses an attached copy of the six official CSVs. A setup cell
links read-only inputs to the notebook's relative paths and writes generated
tables, figures and cleaned data to
`/kaggle/working/ai-tools-developer-workflows/`. Internet and GPU are disabled.
The original local notebook is preserved; the upload version is generated from it.

To prepare uploads after changing the analysis, run:

```zsh
python prepare_kaggle.py --username mdmeheduzzaman
```

This verifies all six source checksums and creates `.kaggle-build/dataset/` and
`.kaggle-build/notebook/`. The dataset includes official CSVs, schemas, provenance,
the local notebook, report, helper scripts and a saved-results archive. Temporary
upload files are ignored by Git. Credentials, virtual environments and Git history
are excluded.

With the [Kaggle CLI](https://github.com/Kaggle/kaggle-cli) installed and authenticated,
create the private dataset once, then upload and execute the notebook:

```zsh
kaggle datasets create -p .kaggle-build/dataset --keep-tabular
kaggle kernels push -p .kaggle-build/notebook
kaggle kernels status mdmeheduzzaman/ai-tools-in-developers-workflows
```

For subsequent data or project updates, replace `datasets create` with
`kaggle datasets version -p .kaggle-build/dataset -m "Update project files" --keep-tabular`.
The notebook is private by default. Use `--public` when preparing a public notebook;
dataset visibility is controlled separately in Kaggle's sharing settings.

## Data and definitions

| Release | Local response-file shape | Valid AI-use answers | Current-use rate |
|---|---:|---:|---:|
| 2023 | 89,184 × 84 | 87,973 | 44.38% |
| 2024 | 65,437 × 114 | 60,907 | 61.84% |
| 2025 | 49,191 × 172 | 33,720 | 78.50% |

Sources: [2023 survey](https://survey.stackoverflow.co/2023/), [2024 survey](https://survey.stackoverflow.co/2024/), [2025 survey](https://survey.stackoverflow.co/2025/) and their official archive. The 2025 archive differs from the published profile total of 49,019; Bangladesh country counts in the archive are 327 (2024) and 220 (2025), versus 325 and 219 in the profiles. These differences are documented rather than removed to force a match. See the [2024 profile](https://survey.stackoverflow.co/2024/developer-profile) and [2025 profile](https://survey.stackoverflow.co/2025/developers).

“Current use” counts affirmative `AISelect` answers, including all three frequency categories in 2025. Planning-only answers are noncurrent; missing answers remain missing. Complete cases are selected separately for each analysis, and every chart and test reports its n.

The schema crosswalk exposes important differences: 2023 trust is `AIBen`, later trust is `AIAcc`; 2025 measures professional work experience rather than professional coding experience; product questions differ by year. `DevType` is a single main role. Genuine multi-select questions receive nullable indicators per question and year. `Indifferent` sentiment is observed in all three releases, contrary to the original brief's claim of a 2025-only neutral option.

## Analysis scope and method

The notebook follows the handbook's **Sections 0–16**, from problem understanding through exports and next steps. Eight research questions cover current use over time, experience, tools/models, sentiment, roles, Bangladesh, and two inferential experience comparisons.

- **Features:** Retains 63 tool/model choice indicators, 49 main-role indicators and five response-status flags. `favorable_sentiment` is 1 for Favorable/Very favorable and 0 for other valid answers, including Indifferent and Unsure; zero means not classified as favorable, rather than unfavorable. Unanswered sentiment stays missing. Section 8 provides a feature-family inventory and 15 computational validation checks.
- **EDA:** 25 charts cover the descriptive analyses, including 100% stacked sentiment by experience. Three missingness charts and one Spearman heatmap bring the total to 29. Grouped tables report their valid denominators.
- **Inference:** Within-year chi-square tests of AI use × experience band report Cramér's V and expected counts. A 2025 Mann–Whitney test compares work-experience distributions with rank-biserial effect size. Holm correction covers these four primary tests; exploratory correlations form a separate family.
- **Exports:** The notebook generates a **203,812 × 134** cleaned CSV and a dictionary for every column, then checks their contents by readback. Raw records are retained; complete-case exclusions are specific to each analysis.

Alongside the use and sentiment trends, Cramér's V is **0.1411, 0.1491 and 0.0843** for the within-year experience/use associations. Statistical significance alone does not establish practical importance. In 2025, users report a median of **10** work years versus **14** for nonusers (rank-biserial **−0.1527**). Bangladesh's current-use shares are **57.96%, 71.91% and 88.14%**, with valid n of **490, 324 and 194**. These findings describe responding samples.

## Methodological robustness

The main analyses and feature definitions are preserved. Sections 9.7.1, 10.1 and 11.1 add three focused checks:

- **Disjoint geography:** Bangladesh versus Rest of World retains the higher Bangladesh estimate in each release. Rest-of-World current use is **44.30%, 61.03% and 78.44%**, with valid n of **87,483, 58,119 and 33,526**. Both groups report 95% Wilson intervals. The 2024 comparison excludes **2,464** valid AI answers with missing country; the required Global comparison retains them.
- **Experience boundaries:** Alternative 2025 bands assign 5 to the middle group and 10 to the highest group. The descending current-use pattern is **STABLE**, with **n=31,104** unchanged; V changes from **0.0843 to 0.0772**. Stability describes direction, not identical percentages or effect magnitude.
- **Complete-case selection:** The 2025 correlation uses **14,930** complete cases from **49,191** records; **15,076** records answered all four source questions. Included and incomplete records differ on observed age and country/role availability. Among valid AI answers, current use is **96.85% versus 63.91%** (n=14,930 versus 18,790), reinforcing the selected-sample interpretation.

The numerical diagnostics are saved in `results/robustness_checks.csv` and `results/complete_case_profiles.csv`. Section 12 distinguishes reducible choices, partially reducible selection/comparability issues and intrinsic survey-design limitations. No additional geographic test, correlation family, model or population weights are introduced.

## Validation status

All **35 code cells** in the revised notebook executed sequentially in a **fresh local Jupyter kernel**, with 29 figures and rich outputs saved. The feature-validation table passed all 15 checks. Independent checks recompute adoption, sentiment, tool counts, chi-square statistics and the Mann–Whitney comparison from raw files, and check exported indicators, missingness, experience mappings and favorable sentiment. The audit also independently verifies the new disjoint groups, Wilson intervals, alternative bands and complete-case profiles. All existing primary numerical findings and the **203,812 × 134** export are unchanged by this robustness pass.

**Earlier Kaggle execution:** notebook version 1 completed successfully with internet disabled. Its adoption, Bangladesh and sentiment results matched the local outputs exactly; statistical results agreed within a relative tolerance of `1e-9`. That execution predates the handbook-alignment changes and the favorable-sentiment column. The latest notebook is prepared locally; it has not been uploaded or executed on Kaggle. Preparing an upload does not verify remote execution.

Kaggle used **Python 3.13.15**, pandas **2.3.3**, NumPy **2.1.3**, SciPy **1.16.3**, statsmodels **0.15.0**, Matplotlib **3.10.0** and seaborn **0.13.2**. These differ from the pinned local environment; each run records its actual library versions. A local Jupyter **Restart Kernel and Run All** remains a useful check after future edits.

## Limitations

The voluntary surveys have self-selection and coverage bias and do not track the same developers across years. Recruitment through Stack Overflow properties, email/newsletters and social channels is not probability sampling; increasing n cannot remove that selection mechanism. See the [2024 methodology](https://survey.stackoverflow.co/2024/methodology) and [2025 methodology](https://survey.stackoverflow.co/2025/methodology). Question changes, item nonresponse and the broader 2025 experience measure limit strict comparisons. Product and model counts are interpreted within their source question. Bangladesh is a small subset of Global, so its comparison is descriptive; binomial intervals cannot remove participation bias. Observational associations do not establish causation, and the 2025 agent-productivity questions do not represent all AI users.

## Licence and responsible use

**Data source and attribution:** Stack Overflow Developer Survey 2023, 2024 and 2025, published by **Stack Exchange Inc. / Stack Overflow**.

The [publisher's official archive and licence notice](https://github.com/StackExchange/Survey/tree/main/packages/archive) specifies the following terms, including for the 2023 release:

- **Database:** [Open Database License (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
- **Individual contents:** [Database Contents License (DbCL) 1.0](https://opendatacommons.org/licenses/dbcl/1-0/).

Suggested attribution:

> Contains information from the Stack Overflow Developer Survey, Stack Exchange Inc., made available under ODbL 1.0; individual contents under DbCL 1.0.

The raw CSVs retain their original values. The generated `data/processed/cleaned_survey.csv` is an adapted database: it standardizes missing values, harmonizes selected variables, validates experience values and adds indicators. Preserve attribution and notices, and follow the applicable ODbL share-alike requirements when redistributing adapted databases. Exact sources and transformations are documented in `data/manifest.json` and `analysis.ipynb`.

These terms apply to the survey data; this notice does not assign a software licence to the project's code.

Only official sources are used; no third-party mirrors or 2026 survey results are included. Country comparisons are descriptive, Bangladesh is not subdivided into small cells, and no general AI-to-productivity causal claim is made. The optional predictive baseline is omitted because instructor approval has not been supplied.
