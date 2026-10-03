"""Fetch missing official Stack Overflow CSVs and verify recorded sizes and hashes."""
from pathlib import Path
import hashlib
import json
import urllib.request


def ensure_data(root=Path('.')):
    """Keep existing verified files; download missing files atomically, failing on mismatch."""
    root = Path(root)
    manifest = json.loads((root / 'data' / 'manifest.json').read_text())
    for item in manifest:
        destination = root / item['relative_path']
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix('.csv.part')
            print(f"Downloading {item['year']} {item['filename']} from the official archive")
            try:
                request = urllib.request.Request(item['source_url'], headers={'User-Agent': 'Project44-SurveyAnalysis'})
                with urllib.request.urlopen(request, timeout=120) as response, temporary.open('wb') as output:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
                if temporary.stat().st_size != item['bytes']:
                    raise ValueError('Downloaded byte size differs from the recorded release; review before using it.')
                with temporary.open('rb') as stream:
                    checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
                if checksum != item['sha256']:
                    raise ValueError('Official archive content differs from the recorded release; review before using it.')
                temporary.replace(destination)
            except Exception as error:
                temporary.unlink(missing_ok=True)
                raise RuntimeError(f"Download/verification failed. Place {item['filename']} in {destination.parent}. "
                                   f"Official source: {item['source_url']}. Reason: {error}") from error
        if destination.stat().st_size != item['bytes']:
            raise ValueError(f'{destination} differs from the recorded byte size; do not use an incomplete or changed file.')
        with destination.open('rb') as stream:
            checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
        if checksum != item['sha256']:
            raise ValueError(f'{destination} differs from the recorded SHA-256; do not run analysis on unverified replacements.')
    print('All six official CSVs match the byte sizes and SHA-256 hashes in data/manifest.json.')


if __name__ == '__main__':
    ensure_data(Path(__file__).resolve().parent)
