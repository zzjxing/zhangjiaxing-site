from pathlib import Path
import json
import re

public = Path('public')
if not (public / 'index.html').exists():
    raise SystemExit('no public')

print('=== article covers ===')
for p in sorted((public / 'api' / 'articles').glob('*.json')):
    d = json.loads(p.read_text(encoding='utf-8'))
    cover = d.get('cover')
    if cover is None and isinstance(d.get('data'), dict):
        cover = d['data'].get('cover')
    print(p.name, cover)

print('=== site.json avatar/logo ===')
site = json.loads((public / 'api' / 'site.json').read_text(encoding='utf-8'))
print(json.dumps({k: site.get(k) for k in site if 'avatar' in k.lower() or 'logo' in k.lower() or 'img' in k.lower() or k in ('theme', 'site')}, ensure_ascii=False, indent=2)[:2000])

print('=== features covers ===')
feat = json.loads((public / 'api' / 'features.json').read_text(encoding='utf-8'))
if isinstance(feat, list):
    for item in feat[:5]:
        print(item.get('title'), item.get('cover'))
elif isinstance(feat, dict):
    data = feat.get('data') or feat.get('posts') or feat
    print(type(data), str(data)[:500])

print('=== static img files ===')
for p in (public / 'static').rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.jpg', '.png', '.webp', '.gif', '.svg', '.ico'}:
        print(p.relative_to(public))

print('=== unpatched /static in js ===')
js = (public / 'static' / 'js' / '120aa8f8.js').read_text(encoding='utf-8')
bad = sorted(set(re.findall(r'"/static/[^"]+"', js)))
print('bad absolute /static count', len(bad))
for m in bad[:10]:
    print(m)
print('Zs default', re.findall(r'Zs="/[^"]+"', js)[:5])
print('baseURL', re.findall(r'baseURL:"[^"]+"', js)[:3])
print('patched default present', '/zhangjiaxing-site/static/img/dccf965f.jpg' in js)
