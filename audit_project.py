"""Independently check the saved notebook results against official local CSVs.

Run after executing analysis.ipynb: python audit_project.py
This reads files only; it does not download data, change raw responses or run a kernel.
"""
from pathlib import Path
import hashlib
import json

import nbformat
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

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
    print(f"PASS: {len(cells)} executed cells, {images} embedded figures, {markdown} rendered interpretations")

    metrics = json.loads((ROOT / "results/metrics.json").read_text())
    tests = pd.read_csv(ROOT / "results/statistical_tests.csv")
    tops = pd.read_csv(ROOT / "results/top_tools.csv")
    dictionary = pd.read_csv(ROOT / "data/processed/data_dictionary.csv")
    exported = pd.read_csv(ROOT / "data/processed/cleaned_survey.csv", dtype="string")
    assert exported.shape == tuple(metrics["export_shape"])
    assert exported.columns.tolist() == dictionary.column.tolist()
    assert not exported.duplicated(["SurveyYear", "ResponseId"]).any()
    missing_report = pd.read_csv(ROOT / "results/missingness.csv")
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

        sent = clean.AISent.dropna()
        assert {"Indifferent", "Unsure"} <= set(sent)
        s = next(row for row in metrics["sentiment"] if row["year"] == year)
        assert s["n"] == len(sent)
        close(s["favorable_pct"], sent.isin(["Favorable", "Very favorable"]).mean() * 100)
        trust = clean["AIBen" if year == 2023 else "AIAcc"]
        assert trust.equals(saved.trust_accuracy_h)

        years = pd.to_numeric(clean["WorkExp" if year == 2025 else "YearsCodePro"].replace(
            {"Less than 1 year": "0.5", "More than 50 years": "51"}), errors="coerce")
        years = years.where(years.between(0, 70) & (years.mod(1).eq(0) | clean['WorkExp' if year == 2025 else 'YearsCodePro'].eq('Less than 1 year')))
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
        print(f"PASS: {year} adoption, Bangladesh, sentiment, trust, tests, tools and nullable indicators")

    assert total_rows == metrics["raw_rows"] == len(exported)
    assert metrics["raw_unchanged"] is True
    np.testing.assert_allclose(tests.p_adjusted, multipletests(raw_pvalues, method="holm")[1], rtol=1e-9, atol=0)
    experience_table = pd.read_csv(ROOT / "results/experience_summary.csv")
    np.testing.assert_allclose(experience_table["Current user"] + experience_table["Not current user"], 100)
    print(f"PASS: primary-family Holm correction and export/dictionary ({exported.shape[0]:,} × {exported.shape[1]})")
    print("AUDIT CHECKS PASSED. Kernel integration and manual source/definition review remain separate checks.")


if __name__ == "__main__":
    main()
