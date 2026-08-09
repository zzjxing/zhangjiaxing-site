import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const shiji = defineCollection({
	loader: glob({ base: './src/content/shiji', pattern: '**/*.md' }),
	schema: z.object({
		title: z.string(),
		order: z.number(),
		summary: z.string().optional(),
	}),
});

const notes = defineCollection({
	loader: glob({ base: './src/content/notes', pattern: '**/*.md' }),
	schema: z.object({
		title: z.string(),
		date: z.coerce.date(),
		summary: z.string().optional(),
	}),
});

const projects = defineCollection({
	loader: glob({ base: './src/content/projects', pattern: '**/*.md' }),
	schema: z.object({
		title: z.string(),
		summary: z.string(),
		url: z.string().url().optional(),
		status: z.string().optional(),
	}),
});

export const collections = { shiji, notes, projects };
