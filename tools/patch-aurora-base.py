"""Rewrite Aurora SPA absolute paths for GitHub project Pages (subdir root)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
BASE = '/zhangjiaxing-site'


def patch_text(text: str) -> str:
	# Axios API + Vue router history
	text = text.replace('baseURL:"/api"', f'baseURL:"{BASE}/api"')
	text = text.replace('baseURL:"/api/"', f'baseURL:"{BASE}/api"')
	text = text.replace('history:m4("/")', f'history:m4("{BASE}/")')

	# Default covers / lazy assets baked into the SPA bundle
	# Avoid double-prefixing if patch is re-run.
	text = text.replace(f'"{BASE}/static/', '"__BASE_STATIC__/')
	text = text.replace('"/static/', f'"{BASE}/static/')
	text = text.replace("'__BASE_STATIC__/", f"'{BASE}/static/")  # noop safety
	text = text.replace('"__BASE_STATIC__/', f'"{BASE}/static/')

	text = text.replace(f"'{BASE}/static/", "'__BASE_STATIC__/")
	text = text.replace("'/static/", f"'{BASE}/static/")
	text = text.replace("'__BASE_STATIC__/", f"'{BASE}/static/")

	# CSS url(/static/...) inside bundles
	text = text.replace(f'url({BASE}/static/', 'url(__BASE_STATIC__/')
	text = text.replace('url(/static/', f'url({BASE}/static/')
	text = text.replace('url(__BASE_STATIC__/', f'url({BASE}/static/')

	# Favicon / other root assets referenced as absolute paths
	text = text.replace(f'"{BASE}/favicon.ico"', '"__BASE_FAVICON__"')
	text = text.replace('"/favicon.ico"', f'"{BASE}/favicon.ico"')
	text = text.replace('"__BASE_FAVICON__"', f'"{BASE}/favicon.ico"')

	return text


def main() -> None:
	if not PUBLIC.exists():
		raise SystemExit('public/ missing — run hexo generate first')

	patched_js = 0
	for path in (PUBLIC / 'static' / 'js').glob('*.js'):
		orig = path.read_text(encoding='utf-8')
		text = patch_text(orig)
		if text != orig:
			path.write_text(text, encoding='utf-8')
			patched_js += 1

	patched_css = 0
	for path in (PUBLIC / 'static').rglob('*.css'):
		orig = path.read_text(encoding='utf-8')
		text = patch_text(orig)
		if text != orig:
			path.write_text(text, encoding='utf-8')
			patched_css += 1

	patched_html = 0
	for path in PUBLIC.rglob('*.html'):
		orig = path.read_text(encoding='utf-8')
		text = patch_text(orig)
		# html also uses src="/static/..." form without quotes variants already covered
		text = text.replace(f'href="{BASE}/favicon.ico"', 'href="__BASE_FAVICON__"')
		text = text.replace('href="/favicon.ico"', f'href="{BASE}/favicon.ico"')
		text = text.replace('href="__BASE_FAVICON__"', f'href="{BASE}/favicon.ico"')
		text = text.replace(f'src="{BASE}/static/', 'src="__BASE_STATIC__/')
		text = text.replace('src="/static/', f'src="{BASE}/static/')
		text = text.replace('src="__BASE_STATIC__/', f'src="{BASE}/static/')
		text = text.replace(f'href="{BASE}/static/', 'href="__BASE_STATIC__/')
		text = text.replace('href="/static/', f'href="{BASE}/static/')
		text = text.replace('href="__BASE_STATIC__/', f'href="{BASE}/static/')
		if text != orig:
			path.write_text(text, encoding='utf-8')
			patched_html += 1

	# GitHub Pages SPA fallback for deep links
	index = PUBLIC / 'index.html'
	fallback = PUBLIC / '404.html'
	if index.exists():
		fallback.write_text(index.read_text(encoding='utf-8'), encoding='utf-8')

	print(f'patched js={patched_js} css={patched_css} html={patched_html} base={BASE}')


if __name__ == '__main__':
	main()
