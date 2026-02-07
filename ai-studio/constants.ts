import { Repo, DeepDiveData } from './types';

export const REPO_DATA: Repo[] = [
  {
    id: 'autogpt',
    rank: 1,
    name: 'AutoGPT',
    owner: 'AutoGPT',
    description: 'An experimental open-source attempt to make GPT-4 fully autonomous. Pushing the boundaries of what AI agents can do by chaining thoughts.',
    language: 'Python',
    languageColor: '#3572A5',
    stars: '142k',
    hnComments: 450,
    updated: '2h ago',
    isNew: true,
    trend: 'up',
    trendValue: 4,
    category: 'AI Agents'
  },
  {
    id: 'llama-3',
    rank: 2,
    name: 'Llama-3-70b',
    owner: 'meta-llama',
    description: "Official repository for Meta's latest large language model. Optimized for inference and fine-tuning on consumer hardware.",
    language: 'Python',
    languageColor: '#3572A5',
    stars: '25k',
    hnComments: 128,
    updated: '5h ago',
    trend: 'up',
    trendValue: 1,
    category: 'LLM'
  },
  {
    id: 'shadcn',
    rank: 3,
    name: 'shadcn/ui',
    owner: 'shadcn',
    description: 'Beautifully designed components built with Radix UI and Tailwind CSS. Accessible. Customizable. Open Source.',
    language: 'TypeScript',
    languageColor: '#2b7489',
    stars: '54k',
    hnComments: 89,
    updated: '1d ago',
    trend: 'neutral',
    trendValue: 0,
    category: 'Web Dev'
  },
  {
    id: 'rust',
    rank: 4,
    name: 'rust',
    owner: 'rust-lang',
    description: 'Empowering everyone to build reliable and efficient software. A language empowering everyone to build reliable and efficient software.',
    language: 'Rust',
    languageColor: '#dea584',
    stars: '92k',
    hnComments: 312,
    updated: '4h ago',
    isNew: true,
    trend: 'up',
    trendValue: 12,
    category: 'System'
  },
  {
    id: 'bun',
    rank: 5,
    name: 'bun',
    owner: 'oven-sh',
    description: 'Incredibly fast JavaScript runtime, bundler, test runner, and package manager – all in one.',
    language: 'Zig',
    languageColor: '#ec915c',
    stars: '68k',
    hnComments: 76,
    updated: '12h ago',
    trend: 'down',
    trendValue: 2,
    category: 'System'
  },
   {
    id: 'omniparse',
    rank: 6,
    name: 'OmniParse',
    owner: 'adithya-s-k',
    description: 'A fully localized, high-precision data ingestion system for LLMs capable of parsing complex PDFs into structured markdown.',
    language: 'Python',
    languageColor: '#3572A5',
    stars: '2.4k',
    hnComments: 210,
    updated: '4h ago',
    isNew: true,
    trend: 'up',
    trendValue: 142,
    category: 'AI Tools'
  }
];

export const OMNIPARSE_DATA: DeepDiveData = {
  title: 'OmniParse',
  subtitle: 'Fully localized, high-precision data ingestion.',
  description: 'A fully localized, high-precision data ingestion system for LLMs capable of parsing complex PDFs into structured markdown.',
  stars: '2.4k',
  forks: '142',
  tags: ['Python', 'OCR', 'LLM'],
  techAnalysis: 'OmniParse is a completely localized data ingestion system designed to transform unstructured data into structured formats usable by Large Language Models (LLMs). Its core architecture is based on Python, utilizing advanced OCR technology and layout analysis algorithms to accurately process PDF documents containing complex tables, images, and multi-column layouts.',
  capabilities: [
    'Supports PDF, PowerPoint, Word',
    'Integration with LlamaIndex',
    'Dockerized for easy deployment'
  ],
  performance: [
    '0.4s average parsing time per page',
    'Low VRAM requirement (runs on T4)',
    'Batch processing supported'
  ],
  whyItMatters: {
    privacy: 'Native',
    tableExtraction: 'Advanced',
    dependency: 'Moderate',
    license: 'GPL-3.0'
  },
  comments: [
    { user: 'dev_ops_ninja', text: "This solves the biggest pain point of PDF parsing - tables spanning multiple pages. I've been hacking Unstructured.io for weeks to do this." },
    { user: 'legal_eagle', text: "Impressive, but be careful with the GPL license if you're embedding this into a proprietary SaaS product." },
    { user: 'curious_cat', text: "Does this support scanned documents or just digital PDFs? The OCR dependency suggests image-based processing." }
  ]
};

export const TREEMAP_DATA = {
  name: "Tech Pulse",
  children: [
    {
      name: "AI & ML",
      children: [
        { name: "langchain", size: 82000, color: "#7c3aed" },
        { name: "ollama", size: 45000, color: "#06b6d4" },
        { name: "autogen", size: 25000, color: "#0f766e" },
        { name: "llama.cpp", size: 48000, color: "#134e4a" },
        { name: "gpt4all", size: 32000, color: "#115e59" },
      ]
    },
    {
      name: "Frontend",
      children: [
        { name: "shadcn/ui", size: 54000, color: "#06e0f9" },
        { name: "next.js", size: 110000, color: "#1e293b" },
        { name: "htmx", size: 28000, color: "#3b82f6" },
        { name: "astro", size: 35000, color: "#6366f1" },
        { name: "svelte", size: 65000, color: "#f97316" },
      ]
    },
    {
      name: "System",
      children: [
        { name: "bun", size: 68000, color: "#f59e0b" },
        { name: "rust", size: 92000, color: "#ea580c" },
        { name: "docker", size: 70000, color: "#0ea5e9" },
        { name: "kubernetes", size: 105000, color: "#3b82f6" },
      ]
    }
  ]
};
