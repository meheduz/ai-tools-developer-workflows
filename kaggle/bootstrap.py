"""Connect the attached Kaggle dataset to the notebook's relative project paths."""
from pathlib import Path
import json
import os
import shutil
import sys

input_root = Path('/kaggle/input')
matches = [p.parent for p in input_root.rglob('2023_survey_results_public.csv')
           if (p.parent / 'manifest.json').is_file()]
if len(matches) != 1:
    raise RuntimeError('Attach the AI Tools Developer Workflows 2023-2025 dataset; '
                       f'expected one matching input, found {len(matches)}.')
input_folder = matches[0]
work_folder = Path('/kaggle/working/ai-tools-developer-workflows')
(work_folder / 'data').mkdir(parents=True, exist_ok=True)
shutil.copy2(input_folder / 'manifest.json', work_folder / 'data' / 'manifest.json')
for filename in ['download_data.py', 'audit_project.py', 'README.md',
                 'report.md', 'DATA_LICENSE.md', 'requirements.txt']:
    shutil.copy2(input_folder / filename, work_folder / filename)
for item in json.loads((work_folder / 'data' / 'manifest.json').read_text()):
    source = input_folder / f"{item['year']}_{item['filename']}"
    destination = work_folder / item['relative_path']
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        if destination.resolve() != source.resolve():
            raise RuntimeError(f'Unexpected existing link: {destination}')
    elif destination.exists():
        raise RuntimeError(f'Unexpected existing raw file: {destination}')
    else:
        destination.symlink_to(source)
os.chdir(work_folder)
if str(work_folder) not in sys.path:
    sys.path.insert(0, str(work_folder))
print('Attached official data:', input_folder)
print('Writable project and output directory:', work_folder)
print('Raw files remain read-only; the original SHA-256 checks run below.')
