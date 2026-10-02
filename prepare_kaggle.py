"""Build a credential-free Kaggle dataset and notebook from verified local files."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
DATASET_SLUG = 'ai-tools-developer-workflows-2023-2025'
NOTEBOOK_SLUG = 'ai-tools-in-developers-workflows'


def write_json(path, value):
    """Write readable UTF-8 metadata without credentials."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def prepare(username, public=False):
    """Verify inputs, stage official CSVs and create a Kaggle-compatible notebook."""
    if not re.fullmatch(r'[A-Za-z0-9_-]+', username):
        raise ValueError('Use your Kaggle username, not a URL or an API token.')
    dataset = ROOT / '.kaggle-build' / 'dataset'
    notebook = ROOT / '.kaggle-build' / 'notebook'
    dataset.mkdir(parents=True, exist_ok=True)
    notebook.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / 'data' / 'manifest.json').read_text())
    for item in manifest:
        source = ROOT / item['relative_path']
        with source.open('rb') as stream:
            checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
        if checksum != item['sha256'] or source.stat().st_size != item['bytes']:
            raise ValueError(f'Raw input differs from the recorded release: {source}')
        target = dataset / f"{item['year']}_{item['filename']}"
        if target.exists():
            target.unlink()
        # A hard link avoids duplicating 459 MB; uploading reads these files only.
        try:
            target.hardlink_to(source)
        except OSError:
            shutil.copy2(source, target)
    shutil.copy2(ROOT / 'data' / 'manifest.json', dataset / 'manifest.json')
    project_files = ['README.md', 'report.md', 'DATA_LICENSE.md', 'requirements.txt',
                     'download_data.py', 'audit_project.py', 'analysis.ipynb']
    for name in project_files:
        shutil.copy2(ROOT / name, dataset / name)
    # Keep the complete saved analysis available as a small separate archive.
    with zipfile.ZipFile(dataset / 'saved-results.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((ROOT / 'results').iterdir()):
            if path.is_file() and path.suffix in {'.csv', '.json', '.png'}:
                archive.write(path, f'results/{path.name}')
    description = '''# AI Tools in Developers' Workflows — Project 44

Official Stack Overflow Developer Survey releases for **2023, 2024 and 2025**,
with the project notebook, report, downloader, data manifest and saved results.
Prepared by **Mustari Ifthe (2023331050)** and
**Md. Meheduz Zaman (2023331064)**.

## Provenance and file layout
The six year-prefixed CSVs are byte-for-byte copies of the official response and
schema files. `manifest.json` records the original URLs, acquisition date, sizes
and SHA-256 hashes. No Kaggle mirror or 2026 survey responses were used.

| Release | Response rows | Response columns |
|---|---:|---:|
| 2023 | 89,184 | 84 |
| 2024 | 65,437 | 114 |
| 2025 | 49,191 | 172 |

The 2025 official archive differs from the website's 49,019 profile responses.
The notebook documents this discrepancy and changing question wording. Original
missing values are preserved; no synthetic responses are included.

`analysis.ipynb` is the executed local notebook. The separate Kaggle notebook
adds an input-mount setup cell. `saved-results.zip` contains the aggregate tables
and charts; the Kaggle run regenerates cleaned data and results as notebook outputs.

## Publisher and licence
Contains information from the **Stack Overflow Developer Survey, Stack Exchange
Inc.**, made available under **ODbL 1.0**; individual contents under **DbCL 1.0**.
Preserve attribution and applicable share-alike terms when redistributing adapted
databases. The data licence does not assign a software licence to project code.

- [Publisher archive and licence notice](https://github.com/StackExchange/Survey/tree/main/packages/archive)
- [2023 survey](https://survey.stackoverflow.co/2023/)
- [2024 survey](https://survey.stackoverflow.co/2024/)
- [2025 survey](https://survey.stackoverflow.co/2025/)
- [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)
- [DbCL 1.0](https://opendatacommons.org/licenses/dbcl/1-0/)

## Interpretation
These are self-selected survey respondents, not a representative sample of all
developers. Country comparisons are descriptive. Experience and product questions
change across releases, and statistical associations do not establish causation.
'''
    write_json(dataset / 'dataset-metadata.json', {
        'id': f'{username}/{DATASET_SLUG}',
        'title': 'AI Tools Developer Workflows 2023-2025',
        'subtitle': 'Official Stack Overflow survey data and Project 44 analysis',
        'description': description,
        'licenses': [{'name': 'ODbL-1.0'}],
    })
    nb = json.loads((ROOT / 'analysis.ipynb').read_text())
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
    bootstrap = (ROOT / 'kaggle' / 'bootstrap.py').read_text()
    nb['cells'][4:4] = [
        {'cell_type': 'markdown', 'id': 'kaggle-runtime-note', 'metadata': {}, 'source': [
            '### Kaggle execution setup\n',
            'The attached dataset contains the verified official releases. This cell '
            'connects read-only inputs to the relative project paths and directs generated '
            'CSV files and charts to `/kaggle/working/ai-tools-developer-workflows/`. '
            'Internet and GPU are unnecessary.\n']},
        {'cell_type': 'code', 'id': 'kaggle-runtime-setup', 'metadata': {},
         'source': bootstrap.splitlines(keepends=True), 'outputs': [], 'execution_count': None},
    ]
    # Use Kaggle's Python kernel; the setup cell reports its actual library versions.
    nb['metadata']['kernelspec'] = {
        'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
    write_json(notebook / 'analysis.ipynb', nb)
    write_json(notebook / 'kernel-metadata.json', {
        'id': f'{username}/{NOTEBOOK_SLUG}',
        'title': 'AI Tools in Developers Workflows',
        'code_file': 'analysis.ipynb', 'language': 'python', 'kernel_type': 'notebook',
        'is_private': not public, 'enable_gpu': False, 'enable_internet': False,
        'dataset_sources': [f'{username}/{DATASET_SLUG}'],
        'competition_sources': [], 'kernel_sources': [], 'model_sources': [],
    })
    print(f'Dataset upload folder: {dataset.relative_to(ROOT)}')
    print(f'Notebook upload folder: {notebook.relative_to(ROOT)}')
    print(f'Visibility: {"public" if public else "private"}; all six source hashes verified.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', required=True, help='Authenticated Kaggle account name')
    parser.add_argument('--public', action='store_true', help='Prepare a public notebook')
    args = parser.parse_args()
    prepare(args.username, args.public)
