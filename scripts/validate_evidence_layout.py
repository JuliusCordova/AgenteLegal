from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / 'docs' / 'evidence'
required = [base / 'README.md', base / 'generated' / '.gitkeep']
missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
if missing:
    raise SystemExit(f'Missing evidence layout: {missing}')
print('evidence layout OK')
