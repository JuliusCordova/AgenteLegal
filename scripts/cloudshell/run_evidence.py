from __future__ import annotations

import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_ROOT = ROOT / 'docs' / 'evidence' / 'generated'


def run(command: list[str]) -> dict:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        'command': ' '.join(command),
        'returncode': completed.returncode,
        'stdout': completed.stdout,
        'stderr': completed.stderr,
    }


def main() -> None:
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out_dir = EVIDENCE_ROOT / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    checks = {
        'unit_tests': run(['pytest', '-q']),
        'compile': run(['python', '-m', 'compileall', 'app', 'tests', 'scripts']),
        'retrieval_smoke': run(['pytest', '-q', 'tests/test_retrieval.py']),
        'meta_orchestrator': run(['pytest', '-q', 'tests/test_meta_orchestrator.py']),
        'portfolio_grounding': run(['pytest', '-q', 'tests/test_portfolio_domain.py']),
        'cross_domain_demo': run(['pytest', '-q', 'tests/test_cross_domain_demo.py']),
        'gcp_project': run(['gcloud', 'config', 'get-value', 'project']),
        'gcp_account': run(['gcloud', 'config', 'get-value', 'account']),
    }

    bucket = os.getenv('LEGAL_GCS_BUCKET', '')
    if bucket:
        checks['gcs_bucket'] = run(['gcloud', 'storage', 'buckets', 'describe', f'gs://{bucket}'])
        checks['gcs_index_metadata'] = run(['gcloud', 'storage', 'ls', f'gs://{bucket}/index/metadata.json'])

    git_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=ROOT, text=True).strip()

    metadata = {
        'timestamp_utc': ts,
        'git_sha': git_sha,
        'git_branch': git_branch,
        'gcp_project_expected': os.getenv('LEGAL_GCP_PROJECT', 'proyectopersonal-480420'),
        'gcp_region': os.getenv('LEGAL_GCP_REGION', 'us-central1'),
        'gcs_bucket': bucket or None,
        'python': platform.python_version(),
        'checks': {name: result['returncode'] == 0 for name, result in checks.items()},
    }

    (out_dir / 'metadata.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    for name, result in checks.items():
        (out_dir / f'{name}.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

    passed = all(result['returncode'] == 0 for result in checks.values())
    lines = [
        '# Cloud Shell Evidence',
        '',
        f'- Timestamp UTC: `{ts}`',
        f'- Git SHA: `{git_sha}`',
        f'- Branch: `{git_branch}`',
        f"- GCP project: `{metadata['gcp_project_expected']}`",
        f"- GCP region: `{metadata['gcp_region']}`",
        f"- GCS bucket: `{bucket or 'not configured'}`",
        '',
        '## Checks',
        '',
    ]
    for name, result in checks.items():
        state = 'PASS' if result['returncode'] == 0 else 'FAIL'
        lines.append(f'- **{state}** — {name}')
    lines.extend(['', '## Result', '', '**PASS**' if passed else '**FAIL**', ''])
    (out_dir / 'README.md').write_text('\n'.join(lines), encoding='utf-8')

    print(out_dir.relative_to(ROOT))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
