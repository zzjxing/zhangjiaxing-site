"""Rewrite Aurora SPA absolute paths for GitHub project Pages (subdir root)."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
BASE = '/zhangjiaxing-site'
BASE_REL = 'zhangjiaxing-site'  # Vite preload helper prefixes "/" itself


def patch_text(text: str) -> str:
	# Axios API + Vue router history
	text = text.replace('baseURL:"/api"', f'baseURL:"{BASE}/api"')
	text = text.replace('baseURL:"/api/"', f'baseURL:"{BASE}/api"')
	text = text.replace('history:m4("/")', f'history:m4("{BASE}/")')

	# Vite preload helper is originally: function(e){return"/"+e}
	# If deps already start with "/", that becomes "//host/..." (protocol-relative)
	# and the browser tries https://zhangjiaxing-site/... — long hang, About never opens.
	for old in (
		'E7=function(e){return"/"+e}',
		'E7=function(e){return"/"+e.replace(/^\\//,"")}',
		'E7=function(e){return e.charAt(0)==="/"?e:"/"+e}',
	):
		text = text.replace(old, '__E7_PLACEHOLDER__')
	text = text.replace(
		'__E7_PLACEHOLDER__',
		'E7=function(e){return e.charAt(0)==="/"?e:"/"+e}',
	)

	# Absolute asset paths used directly (img src, css url, etc.)
	text = text.replace(f'"{BASE}/static/', '"__BASE_STATIC__/')
	text = text.replace('"/static/', f'"{BASE}/static/')
	text = text.replace('"__BASE_STATIC__/', f'"{BASE}/static/')

	text = text.replace(f"'{BASE}/static/", "'__BASE_STATIC__/")
	text = text.replace("'/static/", f"'{BASE}/static/")
	text = text.replace("'__BASE_STATIC__/", f"'{BASE}/static/")

	# Vite preload deps are quoted WITHOUT a leading slash: "static/js/xxx.js".
	# Keep them without a leading slash so E7's "/" + dep is correct:
	# "zhangjiaxing-site/static/js/x" → "/zhangjiaxing-site/static/js/x"
	text = text.replace(f'"{BASE_REL}/static/js/', '"__REL_STATIC_JS__/')
	text = text.replace(f'"{BASE_REL}/static/css/', '"__REL_STATIC_CSS__/')
	text = text.replace('"static/js/', f'"{BASE_REL}/static/js/')
	text = text.replace('"static/css/', f'"{BASE_REL}/static/css/')
	text = text.replace('"__REL_STATIC_JS__/', f'"{BASE_REL}/static/js/')
	text = text.replace('"__REL_STATIC_CSS__/', f'"{BASE_REL}/static/css/')

	# Root-level css chunk: "static/886a749e.css"
	text = re.sub(
		rf'"(?:static//|{re.escape(BASE_REL)}/static/|{re.escape(BASE)}/static/css/)(886a749e\.css)"',
		rf'"{BASE_REL}/static/\1"',
		text,
	)
	text = re.sub(
		r'"static/([^"/]+\.css)"',
		rf'"{BASE_REL}/static/\1"',
		text,
	)

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


def cache_bust_html(digest: str) -> int:
	"""Point HTML script/link tags at patched assets with a content hash query."""
	count = 0
	pattern = re.compile(
		rf'((?:src|href)=")({re.escape(BASE)}/static/[^"?]+)(?:\?[^"]*)?(")'
	)
	for path in PUBLIC.rglob('*.html'):
		orig = path.read_text(encoding='utf-8')
		text = pattern.sub(rf'\1\2?v={digest}\3', orig)
		if text != orig:
			path.write_text(text, encoding='utf-8')
			count += 1
	return count


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

	# Bust HTML→asset URLs so patched main bundle isn't stuck behind CDN cache.
	main_js = next((PUBLIC / 'static' / 'js').glob('*.js'), None)
	digest = '0'
	if main_js is not None:
		# Prefer the largest bundle (app entry); fall back to first.
		main_js = max((PUBLIC / 'static' / 'js').glob('*.js'), key=lambda p: p.stat().st_size)
		digest = hashlib.sha256(main_js.read_bytes()).hexdigest()[:10]
	busted = cache_bust_html(digest)

	# GitHub Pages SPA fallback for deep links
	index = PUBLIC / 'index.html'
	fallback = PUBLIC / '404.html'
	if index.exists():
		fallback.write_text(index.read_text(encoding='utf-8'), encoding='utf-8')

	print(
		f'patched js={patched_js} css={patched_css} html={patched_html} '
		f'bust={busted} v={digest} base={BASE}'
	)


if __name__ == '__main__':
	main()
