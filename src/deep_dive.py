"""深度分析页面生成器 - 为新上榜项目生成独立的分析页面"""

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from .analyzer import RepoAnalysis
from .history import RankChange
from .dashboard import classify_domain, get_lang_color, format_stars_display, LANG_COLORS


@dataclass
class DeepDiveData:
    """深度分析页面所需数据"""
    repo_name: str
    owner: str
    short_name: str
    description: str
    url: str
    language: str
    stars: str
    stars_today: str
    forks: str
    domain: str
    rank: int
    score: int
    # AI 生成的内容
    ai_summary: Optional[str] = None
    ai_highlights: Optional[list] = None
    ai_use_cases: Optional[str] = None
    # 额外信息
    topics: Optional[list] = None
    license: Optional[str] = None


def generate_deep_dive_html(data: DeepDiveData, date: datetime = None, lang: str = 'zh') -> str:
    """
    生成深度分析页面 HTML

    Args:
        data: DeepDiveData 对象
        date: 日期
        lang: 语言

    Returns:
        完整的 HTML 字符串
    """
    if date is None:
        date = datetime.now()

    date_str = date.strftime('%Y-%m-%d')
    html_lang = 'zh-CN' if lang == 'zh' else 'en'
    lang_color = get_lang_color(data.language)

    # 文本
    texts = {
        'zh': {
            'title': f'{data.short_name} - 深度分析',
            'back': '返回热榜',
            'view_repo': '查看仓库',
            'tech_analysis': '技术解析',
            'ai_generated': 'AI 生成',
            'core_capabilities': '核心能力',
            'why_matters': '为什么值得关注',
            'actionable_idea': '创意建议',
            'start_project': '开始探索',
            'related': '相关推荐',
            'rank': '排名',
            'stars': 'Star 数',
            'today': '今日新增',
            'language': '语言',
            'domain': '领域',
            'score': '评分',
            'footer': '数据来源: GitHub Trending',
        },
        'en': {
            'title': f'{data.short_name} - Deep Dive',
            'back': 'Back to Trending',
            'view_repo': 'View Repository',
            'tech_analysis': 'Technical Analysis',
            'ai_generated': 'AI Generated',
            'core_capabilities': 'Core Capabilities',
            'why_matters': 'Why It Matters',
            'actionable_idea': 'Actionable Idea',
            'start_project': 'Start Exploring',
            'related': 'Related Projects',
            'rank': 'Rank',
            'stars': 'Stars',
            'today': 'Today',
            'language': 'Language',
            'domain': 'Domain',
            'score': 'Score',
            'footer': 'Data Source: GitHub Trending',
        }
    }
    t = texts.get(lang, texts['zh'])

    # AI 内容
    ai_summary_html = ''
    if data.ai_summary:
        highlights_html = ''
        if data.ai_highlights:
            highlights_html = '<ul class="list-disc list-inside text-sm space-y-1 text-slate-400 mt-4">'
            for h in data.ai_highlights:
                highlights_html += f'<li>{h}</li>'
            highlights_html += '</ul>'

        use_cases_html = ''
        if data.ai_use_cases:
            use_cases_html = f'<p class="text-sm text-slate-400 mt-4 pt-4 border-t border-white/5"><strong class="text-white">{"适用场景" if lang == "zh" else "Use Cases"}:</strong> {data.ai_use_cases}</p>'

        ai_summary_html = f'''
        <div class="rounded-xl border border-synapse-border bg-synapse-card overflow-hidden">
            <div class="px-6 py-4 border-b border-synapse-border bg-[#1a2628] flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-glow-amber">auto_awesome</span>
                    <h3 class="text-white font-bold text-lg">{t['tech_analysis']}</h3>
                </div>
                <span class="text-xs font-mono text-text-muted uppercase">{t['ai_generated']}</span>
            </div>
            <div class="p-6 md:p-8 text-slate-300 leading-relaxed">
                <p class="text-base">{data.ai_summary}</p>
                {highlights_html}
                {use_cases_html}
            </div>
        </div>
        '''

    # Topics 标签
    topics_html = ''
    if data.topics:
        tags = ''.join([f'<span class="px-2 py-1 rounded text-xs bg-synapse-border text-text-muted">{topic}</span>' for topic in data.topics[:5]])
        topics_html = f'<div class="flex flex-wrap gap-2 mt-4">{tags}</div>'

    return f'''<!DOCTYPE html>
<html lang="{html_lang}" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']} - {date_str}</title>
    <link rel="icon" href="https://github.githubassets.com/favicons/favicon.svg" type="image/svg+xml">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com?plugins=forms"></script>

    <!-- Tailwind Config -->
    <script>
        tailwind.config = {{
            darkMode: "class",
            theme: {{
                extend: {{
                    colors: {{
                        "synapse-bg": "#0D1117",
                        "synapse-card": "#161B22",
                        "synapse-border": "#30363D",
                        "electric-cyan": "#00E5FF",
                        "muted-mint": "#70FFC9",
                        "glow-amber": "#FFAB00",
                        "text-main": "#C9D1D9",
                        "text-muted": "#8B949E",
                    }},
                    fontFamily: {{
                        "display": ["Inter", "sans-serif"],
                        "mono": ["JetBrains Mono", "monospace"],
                    }},
                    boxShadow: {{
                        'neon-cyan': '0 0 5px theme("colors.electric-cyan"), 0 0 20px theme("colors.electric-cyan")',
                        'neon-amber': '0 0 5px theme("colors.glow-amber"), 0 0 10px rgba(255, 171, 0, 0.5)',
                    }}
                }},
            }},
        }}
    </script>

    <style>
        body {{
            background-color: #0D1117;
            color: #C9D1D9;
        }}

        ::-webkit-scrollbar {{
            width: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: #0D1117;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #30363D;
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #00E5FF;
        }}

        .glass-panel {{
            background: rgba(22, 27, 34, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(48, 54, 61, 0.5);
        }}

        .glass-card {{
            background: rgba(13, 17, 23, 0.6);
            border: 1px solid rgba(48, 54, 61, 0.8);
        }}
    </style>
</head>
<body class="min-h-screen font-display">
    <!-- Top Navigation -->
    <header class="sticky top-0 z-50 w-full border-b border-synapse-border bg-synapse-bg/90 backdrop-blur-md">
        <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-6">
                <a href="../index.html" class="flex items-center gap-3 text-white group">
                    <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-electric-cyan to-blue-600 flex items-center justify-center shadow-neon-cyan">
                        <span class="material-symbols-outlined text-black font-bold" style="font-size: 20px;">trending_up</span>
                    </div>
                    <span class="font-bold text-lg">GitHub<span class="text-electric-cyan">Trending</span></span>
                </a>
            </div>
            <a href="../index.html" class="flex items-center gap-2 text-text-muted hover:text-white transition-colors text-sm">
                <span class="material-symbols-outlined text-lg">arrow_back</span>
                {t['back']}
            </a>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-6 py-8">
        <!-- Breadcrumb -->
        <div class="flex items-center gap-2 mb-8 text-sm text-text-muted">
            <a href="../index.html" class="hover:text-electric-cyan transition-colors">Trending</a>
            <span class="material-symbols-outlined text-base">chevron_right</span>
            <span class="text-white">{data.short_name}</span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <!-- Left Column: Main Content -->
            <div class="lg:col-span-8 flex flex-col gap-6">
                <!-- Hero Card -->
                <div class="glass-panel rounded-xl p-8 relative overflow-hidden">
                    <div class="absolute -top-24 -right-24 w-64 h-64 bg-electric-cyan/10 blur-[80px] rounded-full pointer-events-none"></div>
                    <div class="relative z-10">
                        <div class="flex flex-wrap items-start justify-between gap-4 mb-6">
                            <div class="flex flex-col gap-2">
                                <div class="flex items-center gap-3">
                                    <h1 class="text-4xl md:text-5xl font-black text-white tracking-tight">{data.short_name}</h1>
                                    <span class="bg-glow-amber/10 text-glow-amber border border-glow-amber/20 text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider animate-pulse shadow-neon-amber">NEW</span>
                                </div>
                                <p class="text-text-muted text-lg max-w-2xl">{data.description}</p>
                            </div>
                            <a href="{data.url}" target="_blank" class="flex items-center justify-center w-10 h-10 rounded-lg bg-[#24292e] hover:bg-[#2f363d] text-white border border-white/10 transition-all hover:-translate-y-0.5 shadow-lg" title="View on GitHub">
                                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.065 1.815 2.805 1.29 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.525.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405 1.02 0 2.04.135 3 .405 2.28-1.545 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.92 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.285 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                            </a>
                        </div>

                        <!-- Meta Strip -->
                        <div class="flex flex-wrap items-center gap-6 text-sm text-text-muted border-t border-white/5 pt-4 mt-2">
                            <div class="flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full" style="background: {lang_color}; box-shadow: 0 0 8px {lang_color}80;"></span>
                                <span>{data.language}</span>
                            </div>
                            <div class="flex items-center gap-1.5">
                                <span class="material-symbols-outlined text-lg">star</span>
                                <span class="text-white font-medium">{format_stars_display(data.stars)}</span>
                            </div>
                            <div class="flex items-center gap-1.5">
                                <span class="material-symbols-outlined text-lg text-muted-mint">add</span>
                                <span class="text-muted-mint font-medium">+{data.stars_today}</span>
                            </div>
                            <div class="flex items-center gap-1.5">
                                <span class="material-symbols-outlined text-lg">account_tree</span>
                                <span class="text-white font-medium">{data.forks}</span>
                            </div>
                        </div>
                        {topics_html}
                    </div>
                </div>

                <!-- AI Summary Section -->
                {ai_summary_html}

                <!-- Stats Grid -->
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div class="glass-card rounded-xl p-4">
                        <p class="text-xs text-text-muted mb-1">{t['rank']}</p>
                        <p class="text-2xl font-bold text-electric-cyan">#{data.rank}</p>
                    </div>
                    <div class="glass-card rounded-xl p-4">
                        <p class="text-xs text-text-muted mb-1">{t['score']}</p>
                        <p class="text-2xl font-bold text-muted-mint">{data.score}/10</p>
                    </div>
                    <div class="glass-card rounded-xl p-4">
                        <p class="text-xs text-text-muted mb-1">{t['domain']}</p>
                        <p class="text-xl font-bold text-white">{data.domain}</p>
                    </div>
                </div>
            </div>

            <!-- Right Column: Sidebar -->
            <div class="lg:col-span-4 flex flex-col gap-6">
                <!-- CTA Card -->
                <div class="rounded-xl p-[1px] bg-gradient-to-br from-electric-cyan via-muted-mint to-electric-cyan/20 relative">
                    <div class="absolute inset-0 bg-electric-cyan/20 blur-xl opacity-20"></div>
                    <div class="bg-synapse-bg rounded-[11px] p-6 h-full relative z-10">
                        <div class="w-12 h-12 rounded-full bg-electric-cyan/10 flex items-center justify-center mb-4 text-electric-cyan border border-electric-cyan/20">
                            <span class="material-symbols-outlined text-3xl">code</span>
                        </div>
                        <h4 class="text-white font-bold text-lg mb-2">{t['view_repo']}</h4>
                        <p class="text-text-muted text-sm leading-relaxed mb-6">
                            {data.repo_name}
                        </p>
                        <a href="{data.url}" target="_blank" class="w-full py-2.5 rounded-lg bg-electric-cyan hover:bg-cyan-400 text-black font-bold text-sm transition-colors flex items-center justify-center gap-2">
                            <span>{t['start_project']}</span>
                            <span class="material-symbols-outlined text-lg">rocket_launch</span>
                        </a>
                    </div>
                </div>

                <!-- Maintainer -->
                <div class="glass-card rounded-xl p-4 flex items-center gap-4">
                    <img src="https://github.com/{data.owner}.png?size=80" alt="{data.owner}" class="w-12 h-12 rounded-full ring-1 ring-synapse-border">
                    <div>
                        <p class="text-xs text-text-muted">Maintained by</p>
                        <p class="text-white font-bold">{data.owner}</p>
                    </div>
                </div>

                <!-- Meta Info -->
                <div class="glass-card rounded-xl p-4 space-y-3">
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-text-muted">{t['language']}</span>
                        <span class="text-white font-medium flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full" style="background: {lang_color}"></span>
                            {data.language}
                        </span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-text-muted">{t['domain']}</span>
                        <span class="text-white font-medium">{data.domain}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-text-muted">{t['stars']}</span>
                        <span class="text-white font-medium">{data.stars}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm">
                        <span class="text-text-muted">{t['today']}</span>
                        <span class="text-muted-mint font-medium">+{data.stars_today}</span>
                    </div>
                    {f'<div class="flex justify-between items-center text-sm"><span class="text-text-muted">License</span><span class="text-white font-mono text-xs bg-synapse-border px-2 py-1 rounded">{data.license}</span></div>' if data.license else ''}
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-synapse-border bg-synapse-bg mt-12 py-8">
        <div class="max-w-6xl mx-auto px-6 text-center text-text-muted text-sm">
            <p>{t['footer']} • {date_str}</p>
        </div>
    </footer>
</body>
</html>
'''


def generate_deep_dive_pages(analyses: list[RepoAnalysis],
                             rank_changes: list[RankChange],
                             ai_summaries: dict = None,
                             base_dir: str = 'archives',
                             date: datetime = None,
                             lang: str = 'zh') -> list[str]:
    """
    为新上榜项目生成深度分析页面

    Args:
        analyses: 分析结果列表
        rank_changes: 排名变化列表
        ai_summaries: AI 摘要字典
        base_dir: 输出目录
        date: 日期
        lang: 语言

    Returns:
        生成的文件路径列表
    """
    if date is None:
        date = datetime.now()

    if ai_summaries is None:
        ai_summaries = {}

    # 创建 deep-dive 目录
    deep_dive_dir = Path(base_dir) / 'deep-dive'
    deep_dive_dir.mkdir(parents=True, exist_ok=True)

    # 找出新上榜项目
    change_map = {c.name: c for c in rank_changes}
    sorted_analyses = sorted(analyses, key=lambda x: x.score, reverse=True)[:25]

    generated_files = []

    for i, analysis in enumerate(sorted_analyses, 1):
        repo = analysis.repo
        change = change_map.get(repo.name)

        # 只为新项目生成
        if not (change and change.is_new):
            continue

        owner = repo.name.split('/')[0] if '/' in repo.name else repo.name
        short_name = repo.name.split('/')[-1] if '/' in repo.name else repo.name

        ai = ai_summaries.get(repo.name)

        data = DeepDiveData(
            repo_name=repo.name,
            owner=owner,
            short_name=short_name,
            description=repo.description,
            url=repo.url,
            language=repo.language or 'Unknown',
            stars=repo.stars,
            stars_today=repo.stars_today,
            forks=repo.forks,
            domain=classify_domain(repo.name, repo.description, repo.language or ''),
            rank=i,
            score=analysis.score,
            ai_summary=ai.summary if ai else None,
            ai_highlights=ai.highlights if ai else None,
            ai_use_cases=ai.use_cases if ai else None,
            topics=analysis.topics if hasattr(analysis, 'topics') else None,
            license=analysis.license if hasattr(analysis, 'license') else None,
        )

        html = generate_deep_dive_html(data, date, lang)

        # 使用安全的文件名
        safe_name = short_name.lower().replace(' ', '-').replace('/', '-')
        file_path = deep_dive_dir / f'{safe_name}.html'

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)

        generated_files.append(str(file_path))
        print(f'  Generated deep dive: {file_path}')

    return generated_files
