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
	text = text.replace('"__BASE_STATIC__/', f'"{BASE}/static/')

	text = text.replace(f"'{BASE}/static/", "'__BASE_STATIC__/")
	text = text.replace("'/static/", f"'{BASE}/static/")
	text = text.replace("'__BASE_STATIC__/", f"'{BASE}/static/")

	# Vite preload deps are quoted WITHOUT a leading slash: "static/js/xxx.js".
	# On /about/ those resolve to /about/static/... and break the page.
	text = text.replace(f'"{BASE}/static/js/', '"__BASE_STATIC_JS__/')
	text = text.replace(f'"{BASE}/static/css/', '"__BASE_STATIC_CSS__/')
	text = text.replace('"static/js/', f'"{BASE}/static/js/')
	text = text.replace('"static/css/', f'"{BASE}/static/css/')
	text = text.replace('"__BASE_STATIC_JS__/', f'"{BASE}/static/js/')
	text = text.replace('"__BASE_STATIC_CSS__/', f'"{BASE}/static/css/')

	# CSS url(/static/...) inside bundles
	text = text.replace(f'url({BASE}/static/', 'url(__BASE_STATIC__/')
	text = text.replace('url(/static/', f'url({BASE}/static/')
	text = text.replace('url(__BASE_STATIC__/', f'url({BASE}/static/')

	# Favicon / other root assets referenced as absolute paths
	text = text.replace(f'"{BASE}/favicon.ico"', '"__BASE_FAVICON__"')
	text = text.replace('"/favicon.ico"', f'"{BASE}/favicon.ico"')
	text = text.replace('"__BASE_FAVICON__"', f'"{BASE}/favicon.ico"')

	# Home "horizontal article" hero (shown when theme.feature is false).
	# Remove it and keep the first post in the normal card grid.
	text = text.replace(
		':(O(),be(l,{key:1,class:"mb-8",data:e.posts.data[0]||{}},null,8,["data"]))',
		':fe("",!0)',
	)
	text = text.replace(
		':(O(!0),$(me,{key:1},Ue(e.posts.data,(T,P)=>(O(),$(me,{key:T.slug},[P!==0?(O(),$("li",c_,[R(h,{data:T},null,8,["data"])])):fe("",!0)],64))),128))',
		':(O(!0),$(me,{key:1},Ue(e.posts.data,T=>(O(),$("li",{key:T.slug},[R(h,{data:T},null,8,["data"])]))),128))',
	)

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
