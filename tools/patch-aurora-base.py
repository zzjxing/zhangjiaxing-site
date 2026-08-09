"""Rewrite Aurora SPA absolute paths for GitHub project Pages (subdir root)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
BASE = '/zhangjiaxing-site'


def main() -> None:
	if not PUBLIC.exists():
		raise SystemExit('public/ missing — run hexo generate first')

	js_files = list((PUBLIC / 'static' / 'js').glob('*.js'))
	patched_js = 0
	for path in js_files:
		text = path.read_text(encoding='utf-8')
		orig = text
		text = text.replace('baseURL:"/api"', f'baseURL:"{BASE}/api"')
		text = text.replace('baseURL:"/api/"', f'baseURL:"{BASE}/api"')
		text = text.replace('history:m4("/")', f'history:m4("{BASE}/")')
		if text != orig:
			path.write_text(text, encoding='utf-8')
			patched_js += 1

	patched_html = 0
	for path in PUBLIC.rglob('*.html'):
		text = path.read_text(encoding='utf-8')
		orig = text
		text = text.replace('href="/favicon.ico"', f'href="{BASE}/favicon.ico"')
		text = text.replace('src="/static/', f'src="{BASE}/static/')
		text = text.replace('href="/static/', f'href="{BASE}/static/')
		if text != orig:
			path.write_text(text, encoding='utf-8')
			patched_html += 1

	# GitHub Pages SPA fallback for deep links
	index = PUBLIC / 'index.html'
	fallback = PUBLIC / '404.html'
	if index.exists():
		fallback.write_text(index.read_text(encoding='utf-8'), encoding='utf-8')

	print(f'patched js={patched_js} html={patched_html} base={BASE}')


if __name__ == '__main__':
	main()
