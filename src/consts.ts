// Site-wide settings. Edit this file to rebrand the theme — every page,
// the RSS feed, and Open Graph tags read from here.

import type { UIKey } from './i18n/en';

export const SITE = {
	locale: 'zh-CN',
	title: 'zjx',
	description: 'zjx',
	rssDescription: 'zjx',
	ogImage: '/og.jpg',
	author: 'zjx',
	footerText: 'zjx',
} as const;

/** Icons bundled with the theme — see `src/components/SocialLinks.astro`. */
export type SocialIcon = 'github' | 'x' | 'linkedin' | 'rss' | 'email';

export interface SocialLink {
	/** Accessible name announced on the icon-only link. */
	label: string;
	/** Full URL, `mailto:` address, or site-root path (gets `base` applied). */
	href: string;
	icon: SocialIcon;
}

/** Social profiles rendered as inline SVG icons in the footer.
 *  Add or remove entries here — no template edits needed. */
export const SOCIAL_LINKS: readonly SocialLink[] = [
	{ label: 'GitHub', href: 'https://github.com/zzjxing', icon: 'github' },
	{ label: 'RSS', href: '/rss.xml', icon: 'rss' },
];

/** Giscus — GitHub Discussions-backed comments on blog posts.
 *  See `GISCUS` below; values come from https://giscus.app. */
export interface GiscusConfig {
	/** Master switch. While `false`, no Giscus markup, CSS, or script is emitted. */
	enabled: boolean;
	/** Target repository, `owner/name`. Needs public Discussions and the
	 *  giscus GitHub App installed. */
	repo: string;
	/** Repository ID from giscus.app (starts with `R_`). */
	repoId: string;
	/** Discussion category name, e.g. `Announcements`. */
	category: string;
	/** Category ID from giscus.app (starts with `DIC_`). */
	categoryId: string;
	/** How a post maps to its discussion. `pathname` is the safest default —
	 *  it survives retitling, unlike `title`. */
	mapping: 'pathname' | 'url' | 'title' | 'og:title' | 'specific' | 'number';
	/** Use a strict title match when looking up the discussion. */
	strict: boolean;
	/** Show the reaction bar above the comment list. */
	reactionsEnabled: boolean;
	/** Put the comment box above (`top`) or below (`bottom`) the thread. */
	inputPosition: 'top' | 'bottom';
	/** Giscus UI language, e.g. `en`, `ja`, `fr`. */
	lang: string;
	/** Giscus theme used while the site is in light mode. */
	lightTheme: string;
	/** Giscus theme used while the site is in dark mode. The widget is told to
	 *  switch live when the header toggle flips. */
	darkTheme: string;
}

/** Comments are **off by default** — the theme ships no third-party JavaScript
 *  unless you ask for it. To turn them on: enable Discussions on your repo,
 *  install the giscus app (https://github.com/apps/giscus), fill in the IDs
 *  from https://giscus.app, and set `enabled: true`. */
export const GISCUS: GiscusConfig = {
	enabled: false,
	repo: '',
	repoId: '',
	category: 'Announcements',
	categoryId: '',
	mapping: 'pathname',
	strict: true,
	reactionsEnabled: true,
	inputPosition: 'bottom',
	lang: 'zh-CN',
	lightTheme: 'light',
	darkTheme: 'dark',
};

export type NavItem =
	| { href: string; label: string; labelKey?: never }
	| { href: string; labelKey: UIKey; label?: never };

/** Header navigation. `href` is relative to the site root; the configured
 *  `base` is applied automatically via `withBase()`. The bundled entries
 *  localize through the UI dictionary; give a page you add yourself a literal
 *  `label` instead — one of the two is required. */
export const NAV_ITEMS: readonly NavItem[] = [
	{ href: '/', label: '首页' },
	{ href: '/shiji/', label: '史记' },
	{ href: '/blog/', label: '笔记' },
	{ href: '/works/', label: '项目' },
	{ href: '/about/', label: '关于' },
	{ href: '/search/', label: '搜索' },
];
