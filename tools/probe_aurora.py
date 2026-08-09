from pathlib import Path

t = Path('node_modules/hexo-theme-aurora/source/static/js/120aa8f8.js').read_text(
    encoding='utf-8', errors='ignore'
)
j = t.find('async function Rp(){return ft.get("/site.json")}')
print(t[j - 500 : j + 200])
print('====')
# find ft=
for pat in ['ft=Yt', 'ft=ax', 'const ft', 'let ft', 'ft=q', 'ft=Oe', 'ft=new', 'ft=Yt.create', '.create({baseURL']:
    i = t.find(pat)
    print(pat, i)
# reverse search assignment to ft before site.json
chunk = t[:j]
# last 'ft=' before
idx = chunk.rfind('ft=')
print('last ft=', idx, chunk[idx : idx + 200] if idx >= 0 else None)
idx = chunk.rfind('=Yt.create')
print('Yt.create', idx, chunk[idx - 30 : idx + 120] if idx >= 0 else None)
