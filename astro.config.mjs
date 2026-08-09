import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import pagefind from 'astro-pagefind';
import siteConfig from './src/site.config.ts';

export default defineConfig({
	site: 'https://zzjxing.github.io',
	base: '/zhangjiaxing-site',
	integrations: [
		mdx(),
		...(siteConfig.features.sitemap ? [sitemap()] : []),
		...(siteConfig.features.search ? [pagefind()] : []),
	],
	output: 'static',
	trailingSlash: 'always',
	build: {
		format: 'directory',
		inlineStylesheets: 'auto',
	},
	vite: {
		build: {
			cssMinify: true,
		},
	},
	image: {
		service: {
			entrypoint: 'astro/assets/services/sharp',
		},
		format: ['avif', 'webp'],
	},
	server: {
		port: 3000,
		host: true,
	},
	devToolbar: {
		enabled: false,
	},
});
