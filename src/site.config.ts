export interface SiteConfig {
	name: string;
	title: string;
	description: string;
	author: string;
	url: string;
	ogImage: string;
	twitterHandle: string;
	lang: string;
	ogLocale?: string;
	theme: {
		accentColor: string;
		defaultColorMode: 'light' | 'dark' | 'system';
		showThemeToggle: boolean;
	};
	nav: {
		main: Array<{
			name: string;
			href: string;
		}>;
	};
	features: {
		blog: boolean;
		portfolio: boolean;
		landing: boolean;
		rss: boolean;
		sitemap: boolean;
		search: boolean;
	};
	social: {
		github?: string;
		twitter?: string;
		linkedin?: string;
		instagram?: string;
		youtube?: string;
	};
	blog: {
		postsPerPage: number;
		showToc: boolean;
		showReadingTime: boolean;
		showShareButtons: boolean;
		showRelatedPosts: boolean;
	};
	portfolio: {
		projectsPerPage: number;
		showTechStack: boolean;
		showYear: boolean;
	};
	footer: {
		links: Array<{
			name: string;
			href: string;
		}>;
	};
}

const siteConfig: SiteConfig = {
	name: 'zjx',
	title: 'zjx',
	description: 'zjx',
	author: 'zjx',
	url: 'https://zzjxing.github.io/zhangjiaxing-site',
	ogImage: '/og-image.png',
	twitterHandle: '',
	lang: 'zh-CN',
	ogLocale: 'zh_CN',

	theme: {
		accentColor: 'hsl(162, 42%, 38%)',
		defaultColorMode: 'system',
		showThemeToggle: true,
	},

	nav: {
		main: [
			{ name: '首页', href: '/' },
			{ name: '史记', href: '/shiji/' },
			{ name: '笔记', href: '/blog/' },
			{ name: '项目', href: '/work/' },
			{ name: '关于', href: '/about/' },
		],
	},

	features: {
		blog: true,
		portfolio: true,
		landing: false,
		rss: true,
		sitemap: true,
		search: true,
	},

	social: {
		github: 'https://github.com/zzjxing',
	},

	blog: {
		postsPerPage: 6,
		showToc: true,
		showReadingTime: false,
		showShareButtons: false,
		showRelatedPosts: false,
	},

	portfolio: {
		projectsPerPage: 9,
		showTechStack: true,
		showYear: true,
	},

	footer: {
		links: [
			{ name: 'GitHub', href: 'https://github.com/zzjxing' },
			{ name: 'RSS', href: '/rss.xml' },
		],
	},
};

const COMMON_REGIONS: Record<string, string> = {
	en: 'US',
	ja: 'JP',
	zh: 'CN',
	fr: 'FR',
	de: 'DE',
	es: 'ES',
	pt: 'PT',
	ko: 'KR',
	it: 'IT',
	ru: 'RU',
	ar: 'SA',
	nl: 'NL',
	pl: 'PL',
	tr: 'TR',
	vi: 'VN',
	th: 'TH',
	id: 'ID',
	hi: 'IN',
};

export function deriveOgLocale(lang: string): string {
	const [language, region] = lang.split('-');
	const fallbackRegion = COMMON_REGIONS[language.toLowerCase()] ?? language;
	return `${language}_${(region ?? fallbackRegion).toUpperCase()}`;
}

export const resolvedOgLocale =
	siteConfig.ogLocale ?? deriveOgLocale(siteConfig.lang);

export default siteConfig;
