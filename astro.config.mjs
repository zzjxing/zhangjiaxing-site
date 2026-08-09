// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import { remarkReadingTime } from './remark-reading-time.mjs';

// https://astro.build/config
export default defineConfig({
	site: 'https://zzjxing.github.io',
	base: '/zhangjiaxing-site',
	integrations: [mdx(), sitemap()],
	trailingSlash: 'always',
	markdown: {
		processor: unified({
			remarkPlugins: [remarkReadingTime],
		}),
		shikiConfig: {
			themes: {
				light: 'github-light',
				dark: 'github-dark',
			},
			defaultColor: false,
			wrap: true,
		},
	},
});
