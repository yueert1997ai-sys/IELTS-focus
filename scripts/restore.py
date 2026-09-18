"""Restore the complete v4.0 source byte-for-byte; stop on any mismatch.
Uses only the Python standard library. No network access or account credentials.
"""
from pathlib import Path
import hashlib
import json
import lzma
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = '4921cab4583ae861b073f6eb9eda5d07244e6c887f41ff96744450893228a1f6'
m = json.loads((ROOT / 'source/manifest.json').read_text(encoding='utf-8'))
if m['sha256'] != EXPECTED or m['bytes'] != 391765:
    raise SystemExit('Unexpected source manifest')
parts = []
for i, p in enumerate(m['parts']):
    path = f'source/v4.0.part{i:02d}.xz'
    if p['path'] != path:
        raise SystemExit('Unexpected part ordering or path')
    b = (ROOT / path).read_bytes()
    git_sha = hashlib.sha1(f'blob {len(b)}\0'.encode() + b).hexdigest()
    if len(b) != p['size'] or git_sha != p['git_sha']:
        raise SystemExit(f'Corrupt source part: {path}')
    parts.append(b)
raw = lzma.decompress(b''.join(parts), format=lzma.FORMAT_XZ, memlimit=256*1024*1024)
if len(raw) != m['bytes'] or hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit('Full-source checksum mismatch; refusing to publish')
html = raw.decode('utf-8')
comp = re.search(r'const BANK = (\{.*?\});\s*const APP_VERSION', html, re.S)
pre = re.search(r'<script\b[^>]*id=[\"\']preload-data[\"\'][^>]*>(.*?)</script>', html, re.S)
if not comp or not pre:
    raise SystemExit('Question banks missing')
c, d = json.loads(comp[1]), json.loads(pre[1])
counts = {
    'compression_single_questions': sum(len(s['items']) for s in c['single']),
    'compression_matching_sets': len(c['matching']),
    'preload_themes': len(d['packs']),
    'preload_single_questions': sum(len(p['singles']) for p in d['packs']),
    'preload_choose_two_sets': sum(bool(p.get('multi')) for p in d['packs']),
    'preload_matching_questions': sum(len(p['matching']['items']) for p in d['packs']),
}
for key, value in counts.items():
    if value != m[key]:
        raise SystemExit(f'Question count mismatch: {key}')
for forbidden in ('supabase', 'aidocmaker', 'cdn.jsdelivr.net'):
    if forbidden in html.lower():
        raise SystemExit(f'Unexpected external dependency: {forbidden}')
script_count = 0
with tempfile.TemporaryDirectory() as directory:
    for attrs, text in re.findall(r'<script\b([^>]*)>(.*?)</script>', html, re.S):
        if 'application/json' in attrs.lower():
            continue
        if re.search(r'\bsrc\s*=', attrs, re.I):
            raise SystemExit('Unexpected external script')
        f = Path(directory) / f'script-{script_count}.js'
        f.write_text(text, encoding='utf-8')
        subprocess.run(['node', '--check', str(f)], check=True)
        script_count += 1
# Only write after all checks pass. The output is exactly the approved full source.
(ROOT / 'index.html').write_bytes(raw)
site = ROOT / '_site'
site.mkdir(exist_ok=True)
(site / 'index.html').write_bytes(raw)
(site / '.nojekyll').write_text('', encoding='utf-8')
report = {'version':m['version'], 'bytes':len(raw), 'sha256':EXPECTED,
          'question_counts':counts, 'scripts_syntax_checked':script_count,
          'network_dependencies':[], 'cloud_sync':False}
(site / 'integrity.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
