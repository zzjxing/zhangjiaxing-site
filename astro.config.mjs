// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages project site: https://<user>.github.io/zhangjiaxing-site/
// If you later rename the repo to <user>.github.io, set base to '/'.
export default defineConfig({
	site: 'https://zzjxing.github.io',
	base: '/zhangjiaxing-site',
	trailingSlash: 'always',
});
