"""Independently check the saved notebook results against official local CSVs.

Run after executing analysis.ipynb: python audit_project.py
This reads files only; it does not download data, change raw responses or run a kernel.
"""
from pathlib import Path
import hashlib
import json
import re

import nbformat
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint

ROOT = Path(__file__).resolve().parent
YEARS = (2023, 2024, 2025)
MISSING = {"", "NA", "N/A", "nan"}
TOOLS = {2023: ["AISearchHaveWorkedWith", "AIDevHaveWorkedWith"],
         2024: ["AISearchDevHaveWorkedWith"], 2025: ["AIModelsHaveWorkedWith"]}


def close(actual, expected):
    """Require numerical agreement including very small p-values, without absolute tolerance."""
    assert np.isclose(actual, expected, rtol=1e-9, atol=0, equal_nan=True), (actual, expected)


def main():
    manifest = json.loads((ROOT / "data/manifest.json").read_text())
    for entry in manifest:
        path = ROOT / entry["relative_path"]
        assert path.stat().st_size == entry["bytes"], path
        with path.open("rb") as stream:
            assert hashlib.file_digest(stream, "sha256").hexdigest() == entry["sha256"], path
    print("PASS: all six source sizes and SHA-256 hashes")

    notebook = nbformat.read(ROOT / "analysis.ipynb", as_version=4)
    nbformat.validate(notebook)
    cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert [cell.execution_count for cell in cells] == list(range(1, len(cells) + 1))
    for cell in cells:
        compile(cell.source, "<notebook cell>", "exec")
        assert not any(o.output_type == "error" for o in cell.outputs)
    images = sum("image/png" in output.get("data", {}) for cell in cells for output in cell.outputs)
    markdown = sum("text/markdown" in output.get("data", {}) for cell in cells for output in cell.outputs)
    assert images >= 8 and markdown >= 16
    assert len(list((ROOT / "results").glob("*.png"))) == images
    print(f"PASS: {len(cells)} executed cells, {images} embedded figures, {markdown} rendered Markdown outputs")

    prose = '\n'.join(cell.source for cell in notebook.cells if cell.cell_type == 'markdown')
    headings = re.findall(r'^#{1,2} (\d+)\. ', prose, flags=re.MULTILINE)
    assert headings == [str(n) for n in range(17)], headings
    assert 'Student Checkpoint' in prose and 'IMPORTANT CLARIFICATION' in prose and 'KEY LESSON' in prose
    cleaning = prose.split('## 7. Data Cleaning', 1)[1].split('## 8. Feature Engineering', 1)[0]
    steps = re.split(r'^### 7\.\d+ ', cleaning, flags=re.MULTILINE)[1:]
    assert len(steps) >= 6
    for step in steps:
        assert all(f'**{label}:**' in step for label in ['Problem', 'Action', 'Reason', 'Validation'])
    assert 'sentiment_experience_' in '\n'.join(cell.source for cell in cells)
    for year in YEARS:
        assert (ROOT / f'results/sentiment_experience_{year}.png').is_file()
    print('PASS: Sections 0–16, answered checkpoint, nine documented cleaning steps and sentiment charts')

    metrics = json.loads((ROOT / "results/metrics.json").read_text())
    tests = pd.read_csv(ROOT / "results/statistical_tests.csv")
    tops = pd.read_csv(ROOT / "results/top_tools.csv")
    dictionary = pd.read_csv(ROOT / "data/processed/data_dictionary.csv")
    exported = pd.read_csv(ROOT / "data/processed/cleaned_survey.csv", dtype="string")
    assert exported.shape == tuple(metrics["export_shape"])
    assert exported.columns.tolist() == dictionary.column.tolist()
    assert not exported.duplicated(["SurveyYear", "ResponseId"]).any()
    tool_choices = [col for col in exported if col.startswith('tool_') and '__' in col and not col.endswith('__answered')]
    role_choices = [col for col in exported if col.startswith('role__') and not col.endswith('__answered')]
    status_flags = [col for col in exported if col.endswith('__answered')]
    assert len(tool_choices) == 63 and len(role_choices) == 49 and len(status_flags) == 5
    validation = pd.read_csv(ROOT / 'results/feature_validation.csv')
    assert validation.Status.eq('PASS').all()
    assert validation['Records checked'].ge(validation['Nonmissing source observations']).all()
    inventory = pd.read_csv(ROOT / 'results/feature_inventory.csv')
    assert inventory.columns.tolist() == ['Feature / family','Source variable(s)','Construction','Data type',
                                         'Purpose','Missing-value behavior','Limitation','Downstream use']
    assert len(inventory) >= 4 and inventory.notna().all().all()
    summary = pd.read_csv(ROOT / 'results/summary_results.csv')
    assert len(summary) == len(metrics['findings']) == 7
    assert summary['Key Result'].tolist() == metrics['findings']
    assert all((ROOT / f'results/{name}.csv').is_file() for name in
               ['experience_summary','sentiment_summary','bangladesh_summary','top_tools','role_summary'])
    missing_report = pd.read_csv(ROOT / "results/missingness.csv")
    robustness = pd.read_csv(ROOT / 'results/robustness_checks.csv')
    profiles = pd.read_csv(ROOT / 'results/complete_case_profiles.csv')
    summary_cells = [c for c in cells if 'robustness_summary=pd.DataFrame' in c.source]
    assert len(summary_cells) == 1 and summary_cells[0].outputs
    raw_pvalues = []
    total_rows = 0

    for year in YEARS:
        raw = pd.read_csv(ROOT / f"data/raw/{year}/survey_results_public.csv", dtype="string", keep_default_na=False)
        clean = raw.apply(lambda col: col.str.strip().mask(col.str.strip().isin(MISSING)))
        missing = missing_report[missing_report.year.eq(year)].set_index("column")
        assert set(missing.index) == set(raw.columns)
        for col in clean:
            assert missing.loc[col, "missing_n"] == int(clean[col].isna().sum())
            close(missing.loc[col, "missing_pct"], clean[col].isna().mean()*100)
        saved = exported[exported.SurveyYear.eq(str(year))].reset_index(drop=True)
        assert len(raw) == len(saved)
        total_rows += len(raw)
        assert raw.ResponseId.equals(saved.ResponseId)
        assert not clean.ResponseId.isna().any() and not clean.ResponseId.duplicated().any()
        assert not raw.duplicated().any()
        assert not clean.DevType.str.contains(";", regex=False, na=False).any()

        answer = clean.AISelect
        if year < 2025:
            assert set(answer.dropna()) == {"Yes", "No, and I don't plan to", "No, but I plan to soon"}
        else:
            assert len(set(answer.dropna())) == 5
        # Different implementation from the notebook's exact label mapping.
        uses = answer.str.startswith("Yes").astype("Float64")
        stored_uses = pd.to_numeric(saved.ai_use_binary)
        np.testing.assert_allclose(uses.to_numpy(dtype=float, na_value=np.nan),
                                   stored_uses.to_numpy(dtype=float, na_value=np.nan), equal_nan=True)
        a = next(row for row in metrics["adoption"] if row["SurveyYear"] == year)
        assert a["n"] == int(uses.count()) and a["current_users"] == int(uses.sum())
        close(a["current_use_pct"], float(uses.mean() * 100))
        bd = next(row for row in metrics["bangladesh"] if row["year"] == year and row["sample"] == "Bangladesh")
        bd_uses = uses[clean.Country.eq("Bangladesh")]
        assert bd["n"] == int(bd_uses.count()) and bd["users"] == int(bd_uses.sum())
        close(bd["pct"], float(bd_uses.mean() * 100))

        # Country+AI answerers partition into disjoint groups; Global may include missing country.
        eligible = clean.Country.notna() & uses.notna()
        country_groups = {'Bangladesh': eligible & clean.Country.eq('Bangladesh').fillna(False),
                          'Rest of World': eligible & clean.Country.ne('Bangladesh').fillna(False)}
        assert not (country_groups['Bangladesh'] & country_groups['Rest of World']).any()
        assert ((country_groups['Bangladesh'] | country_groups['Rest of World']) == eligible).all()
        geography = robustness[robustness.analysis.eq('Geography') & robustness.year.eq(year)]
        assert len(geography) == 2 and geography.n.sum() == int(eligible.sum())
        for name, mask in country_groups.items():
            row = geography[geography.group.eq(name)].iloc[0]
            n = int(mask.sum()); count = int(uses.loc[mask].sum())
            assert row.n == n and row.users == count and row.eligible_n == int(eligible.sum())
            assert row.missing_country_among_AI_answers == int((uses.notna() & clean.Country.isna()).sum())
            close(row.pct, 100 * count / n)
            lo, hi = proportion_confint(count, n, alpha=.05, method='wilson')
            close(row.lower_pct, lo * 100); close(row.upper_pct, hi * 100)
            assert 0 <= row.lower_pct <= row.pct <= row.upper_pct <= 100
        for row in [r for r in metrics['bangladesh'] if r['year'] == year]:
            lo, hi = proportion_confint(row['users'], row['n'], alpha=.05, method='wilson')
            close(row['lower_pct'], lo * 100); close(row['upper_pct'], hi * 100)
        close(a['lower_pct'], next(r['lower_pct'] for r in metrics['bangladesh']
                                 if r['year'] == year and r['sample'] == 'Global'))
        close(a['upper_pct'], next(r['upper_pct'] for r in metrics['bangladesh']
                                 if r['year'] == year and r['sample'] == 'Global'))

        sent = clean.AISent.dropna()
        assert {"Indifferent", "Unsure"} <= set(sent)
        s = next(row for row in metrics["sentiment"] if row["year"] == year)
        assert s["n"] == len(sent)
        close(s["favorable_pct"], sent.isin(["Favorable", "Very favorable"]).mean() * 100)
        favorable = clean.AISent.isin(['Favorable', 'Very favorable']).astype('Float64').mask(clean.AISent.isna())
        actual_favorable = pd.to_numeric(saved.favorable_sentiment)
        np.testing.assert_allclose(actual_favorable.to_numpy(dtype=float, na_value=np.nan),
                                   favorable.to_numpy(dtype=float, na_value=np.nan), equal_nan=True)
        assert actual_favorable.isna().equals(clean.AISent.isna())
        expected_score = clean.AISent.map({'Very unfavorable':1,'Unfavorable':2,'Indifferent':3,'Favorable':4,'Very favorable':5})
        np.testing.assert_allclose(pd.to_numeric(saved.sentiment_score).to_numpy(dtype=float,na_value=np.nan),
                                   expected_score.to_numpy(dtype=float,na_value=np.nan),equal_nan=True)
        trust = clean["AIBen" if year == 2023 else "AIAcc"]
        assert trust.equals(saved.trust_accuracy_h)

        years = pd.to_numeric(clean["WorkExp" if year == 2025 else "YearsCodePro"].replace(
            {"Less than 1 year": "0.5", "More than 50 years": "51"}), errors="coerce")
        years = years.where(years.between(0, 70) & (years.mod(1).eq(0) | clean['WorkExp' if year == 2025 else 'YearsCodePro'].eq('Less than 1 year')))
        np.testing.assert_allclose(pd.to_numeric(saved.experience_years).to_numpy(dtype=float,na_value=np.nan),
                                   years.to_numpy(dtype=float,na_value=np.nan),equal_nan=True)
        expected_bands = pd.cut(years, [0,1,6,11,71],right=False,
                                labels=['<1 year','1–5 years','6–10 years','11+ years']).astype('string')
        assert expected_bands.equals(saved.experience_band)
        band = pd.cut(years, [0, 1, 6, 11, 71], right=False)
        valid = pd.DataFrame({"band": band, "use": uses}).dropna()
        table = pd.crosstab(valid.band, valid.use)
        table = table.loc[table.sum(axis=1).gt(0)]
        chi, p, dof, expected = stats.chi2_contingency(table, correction=False)
        row = tests[tests.test.eq(f"Chi-square {year}")].iloc[0]
        assert row.n == len(valid) and row["df"] == dof and expected.min() >= 5
        close(row.statistic, chi); close(row.p_raw, p)
        close(row.effect_size, np.sqrt(chi / (len(valid) * min(table.shape[0]-1, table.shape[1]-1))))
        close(row.min_expected, expected.min())
        raw_pvalues.append(p)

        for source in TOOLS[year]:
            values = clean[source]
            mentions = values.str.split(";").explode().dropna().value_counts()
            top = tops[tops.year.eq(year) & tops.source.eq(source)]
            assert top.question_n.eq(values.count()).all()
            for row in top.itertuples():
                assert row.selected_n == mentions[row.choice]
                close(row.respondent_pct, row.selected_n / values.count() * 100)
            prefix = f"tool_{year}_{source}__"
            for col in exported.columns[exported.columns.str.startswith(prefix)]:
                assert exported.loc[~exported.SurveyYear.eq(str(year)), col].isna().all()
                if col.endswith("__answered"):
                    expected_flag = values.notna().astype(float)
                else:
                    choice = col.split("__", 1)[1]
                    expected_flag = values.map(lambda value: float(choice in value.split(";")) if pd.notna(value) else np.nan)
                actual = pd.to_numeric(saved[col]).to_numpy(dtype=float, na_value=np.nan)
                np.testing.assert_allclose(actual, expected_flag.to_numpy(dtype=float, na_value=np.nan), equal_nan=True)
        primary = TOOLS[year][-1]
        expected_count = clean[primary].map(lambda value: len(set(value.split(';'))) if pd.notna(value) else np.nan)
        np.testing.assert_allclose(pd.to_numeric(saved.tool_count).to_numpy(dtype=float,na_value=np.nan),
                                   expected_count.to_numpy(dtype=float,na_value=np.nan),equal_nan=True)
        for col in exported.columns[exported.columns.str.startswith("role__")]:
            expected_flag = (clean.DevType.notna().astype(float) if col.endswith("__answered") else
                             clean.DevType.eq(col.split("__", 1)[1]).astype("Float64"))
            np.testing.assert_allclose(pd.to_numeric(saved[col]).to_numpy(dtype=float, na_value=np.nan),
                                       expected_flag.to_numpy(dtype=float, na_value=np.nan), equal_nan=True)

        if year == 2025:
            groups = pd.DataFrame({"years": years, "use": uses}).dropna()
            x = groups.loc[groups.use.eq(1), "years"].to_numpy(dtype=float)
            y = groups.loc[groups.use.eq(0), "years"].to_numpy(dtype=float)
            u, p = stats.mannwhitneyu(x, y, alternative="two-sided", method="asymptotic")
            row = tests[tests.test.eq("Mann–Whitney 2025")].iloc[0]
            assert row.n == len(groups)
            close(row.statistic, u); close(row.p_raw, p)
            close(row.effect_size, 2 * u / (len(x)*len(y)) - 1)
            raw_pvalues.append(p)

            # The alternative is a diagnostic on the same complete cases, leaving main bands unchanged.
            alternative = pd.cut(years, [0,1,5,10,71], right=False,
                                 labels=['<1 year','1–4 years','5–9 years','10+ years'])
            assert alternative.isna().equals(years.isna())
            boundaries = pd.cut(pd.Series([0,.5,1,4,5,9,10,70]), [0,1,5,10,71], right=False,
                                labels=['<1 year','1–4 years','5–9 years','10+ years'])
            assert boundaries.astype(str).tolist() == ['<1 year','<1 year','1–4 years','1–4 years',
                                                       '5–9 years','5–9 years','10+ years','10+ years']
            descending = []
            for grouping, categories in [('Main', expected_bands), ('Alternative', alternative)]:
                paired = pd.DataFrame({'band':categories,'use':uses}).dropna()
                tab = pd.crosstab(paired.band, paired.use)
                # Recover numeric band order rather than lexicographic order.
                order = (['<1 year','1–5 years','6–10 years','11+ years'] if grouping == 'Main' else
                         ['<1 year','1–4 years','5–9 years','10+ years'])
                tab = tab.reindex([b for b in order if b in tab.index])
                chi, _, dof, expected = stats.chi2_contingency(tab, correction=False)
                v = np.sqrt(chi / (len(paired) * min(tab.shape[0]-1,tab.shape[1]-1)))
                rows = robustness[robustness.analysis.eq('Experience banding') & robustness.group.eq(grouping)]
                assert len(rows) == len(tab) and rows.n.sum() == len(groups) == len(paired)
                assert set(rows.band) == set(tab.index) and expected.min() >= 5
                for band_name, counts in tab.iterrows():
                    row = rows[rows.band.eq(band_name)].iloc[0]
                    assert row.n == counts.sum() and row.users == counts[1] and row.analysis_n == len(paired)
                    close(row.pct, 100 * counts[1] / counts.sum())
                    close(row.chi_square, chi); close(row.cramers_v, v)
                    assert row['df'] == dof
                    close(row.min_expected, expected.min())
                descending.append((100*tab[1]/tab.sum(axis=1)).is_monotonic_decreasing)
            if all(descending):
                assert rows.outcome.eq('STABLE').all()

            # Independently rebuild the included/excluded observed-characteristic profiles.
            corr_fields = ['ai_use_binary','experience_years','sentiment_score','tool_count']
            complete = saved[corr_fields].notna().all(axis=1)
            source_joint = clean[['AISelect','WorkExp','AISent','AIModelsHaveWorkedWith']].notna().all(axis=1)
            assert (source_joint | ~complete).all()
            eligibility = robustness[robustness.analysis.eq('Correlation eligibility')].set_index('group')
            assert eligibility.loc['Total survey records','n'] == len(clean)
            assert eligibility.loc['Four source questions nonmissing','n'] == int(source_joint.sum())
            assert eligibility.loc['Analytical complete cases','n'] == int(complete.sum())
            for name, mask in [('Included / complete',complete), ('Excluded / incomplete',~complete)]:
                sample = clean.loc[mask]
                values_by_characteristic = {
                    'Age band':sample.Age.where(sample.Age.ne('Prefer not to say')).fillna('Missing/refused'),
                    'Country availability':sample.Country.notna().map({True:'Available',False:'Missing'}),
                    'Role availability':sample.DevType.notna().map({True:'Available',False:'Missing'}),
                    'AI use among valid answers':uses.loc[mask].dropna().map({1:'Current user',0:'Not current user'})}
                for variable, values in values_by_characteristic.items():
                    rows = profiles[profiles.group.eq(name) & profiles.variable.eq(variable)]
                    expected_counts = values.value_counts()
                    assert set(rows.category) == set(expected_counts.index)
                    assert rows['count'].sum() == len(values)
                    assert rows.denominator.eq(len(values)).all()
                    for r in rows.itertuples():
                        assert r.count == expected_counts[r.category]
                        close(r.pct, 100 * r.count / len(values))
            print('PASS: 2025 alternative boundaries/effect sizes and included/excluded correlation profiles')
        print(f"PASS: {year} adoption, Bangladesh, sentiment/favorable mapping, experience, trust, tests, tool counts and nullable indicators")

    assert total_rows == metrics["raw_rows"] == len(exported)
    assert metrics["raw_unchanged"] is True
    np.testing.assert_allclose(tests.p_adjusted, multipletests(raw_pvalues, method="holm")[1], rtol=1e-9, atol=0)
    experience_table = pd.read_csv(ROOT / "results/experience_summary.csv")
    np.testing.assert_allclose(experience_table["Current user"] + experience_table["Not current user"], 100)
    print(f"PASS: primary-family Holm correction and export/dictionary ({exported.shape[0]:,} × {exported.shape[1]})")
    print('PASS: 63 tool/model indicators, 49 role indicators, five status flags, feature inventory and seven results rows')
    print('PASS: disjoint country groups, eligible totals, Wilson intervals and saved robustness tables')
    print("AUDIT CHECKS PASSED. Kernel integration and manual source/definition review remain separate checks.")


if __name__ == "__main__":
    main()
