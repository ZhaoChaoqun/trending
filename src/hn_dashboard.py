"""
Hacker News 仪表板生成器 - Synapse 风格
"""

from datetime import datetime
from pathlib import Path
from .hn_scraper import HNStory, classify_hn_category


def generate_hn_sidebar_html(lang: str = 'zh', active_page: str = 'hn') -> str:
    """生成左侧边栏 HTML (带 HN 导航)"""
    texts = {
        'zh': {
            'feeds': 'GitHub',
            'all': '全部热门',
            'ai_ml': 'AI & ML',
            'frontend': '前端开发',
            'system': '系统底层',
            'hn_section': 'Hacker News',
            'hn_top': 'Top Stories',
            'hn_best': 'Best Stories',
            'insights': '洞察',
            'rising': '上升最快',
            'new_today': '今日新上榜',
        },
        'en': {
            'feeds': 'GitHub',
            'all': 'All Trending',
            'ai_ml': 'AI & ML',
            'frontend': 'Frontend',
            'system': 'System',
            'hn_section': 'Hacker News',
            'hn_top': 'Top Stories',
            'hn_best': 'Best Stories',
            'insights': 'Insights',
            'rising': 'Rising Stars',
            'new_today': 'New Today',
        }
    }
    t = texts.get(lang, texts['zh'])

    # 根据 active_page 设置高亮
    github_active = 'nav-item-active' if active_page == 'github' else 'nav-item text-text-muted hover:text-white hover:bg-synapse-border/30'
    hn_active = 'nav-item-active' if active_page == 'hn' else 'nav-item text-text-muted hover:text-white hover:bg-synapse-border/30'

    return f'''
    <aside class="w-64 h-full flex flex-col glass-panel border-r border-synapse-border shrink-0 z-20">
        <!-- Header / Logo -->
        <div class="h-16 flex items-center px-6 border-b border-synapse-border">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-electric-cyan to-blue-600 flex items-center justify-center shadow-neon-cyan">
                    <span class="material-symbols-outlined text-black font-bold" style="font-size: 20px;">trending_up</span>
                </div>
                <div>
                    <h1 class="font-bold text-lg tracking-tight text-white">Tech<span class="text-electric-cyan">Pulse</span></h1>
                    <p class="text-[10px] text-text-muted font-mono tracking-wider">SYNAPSE v2.0</p>
                </div>
            </div>
        </div>

        <!-- Navigation -->
        <div class="flex-1 overflow-y-auto py-6 flex flex-col gap-2">
            <!-- GitHub Section -->
            <div class="px-4 mb-2">
                <p class="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 px-2">{t['feeds']}</p>
                <a href="index.html" class="{github_active} flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors group" id="github-link">
                    <span class="material-symbols-outlined">grid_view</span>
                    <span class="text-sm font-medium">{t['all']}</span>
                </a>
            </div>

            <!-- Hacker News Section -->
            <div class="px-4 mt-4">
                <p class="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 px-2">
                    <span class="text-glow-amber">Y</span> {t['hn_section']}
                </p>
                <a href="hn.html" class="{hn_active} flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors group">
                    <span class="material-symbols-outlined text-glow-amber">local_fire_department</span>
                    <span class="text-sm font-medium">{t['hn_top']}</span>
                </a>
            </div>
        </div>

        <!-- Footer -->
        <div class="p-4 border-t border-synapse-border">
            <div class="flex items-center gap-2 text-xs text-text-muted">
                <span class="w-2 h-2 rounded-full bg-glow-amber pulse-dot"></span>
                <span class="font-mono">{'HN 数据已同步' if lang == 'zh' else 'HN Data Synced'}</span>
            </div>
        </div>
    </aside>
    '''


def generate_hn_stats_bar(stories: list[HNStory], lang: str = 'zh') -> str:
    """生成顶部统计条"""
    if not stories:
        return ''

    total_score = sum(s.score for s in stories)
    total_comments = sum(s.comments for s in stories)
    avg_score = round(total_score / len(stories)) if stories else 0

    # 分类统计
    categories = {}
    for s in stories:
        cat = classify_hn_category(s.title, s.url)
        categories[cat] = categories.get(cat, 0) + 1
    top_category = max(categories.items(), key=lambda x: x[1])[0] if categories else 'Other'

    def fmt(n):
        if n >= 1000:
            return f'{n/1000:.1f}k'
        return str(n)

    texts = {
        'zh': ['总 Stories', '平均分数', '总评论', '热门分类'],
        'en': ['Total Stories', 'Avg Score', 'Total Comments', 'Top Category']
    }
    t = texts.get(lang, texts['zh'])

    return f'''
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-glow-amber/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-glow-amber">article</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[0]}</p>
                <p class="text-xl font-bold text-white">{len(stories)}</p>
            </div>
        </div>
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-electric-cyan/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-electric-cyan">arrow_upward</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[1]}</p>
                <p class="text-xl font-bold text-white">{avg_score}</p>
            </div>
        </div>
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-muted-mint/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-muted-mint">chat</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[2]}</p>
                <p class="text-xl font-bold text-white">{fmt(total_comments)}</p>
            </div>
        </div>
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-purple-400">category</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[3]}</p>
                <p class="text-xl font-bold text-white">{top_category}</p>
            </div>
        </div>
    </div>
    '''


def generate_hn_story_html(story: HNStory, rank: int, lang: str = 'zh') -> str:
    """生成单个 HN Story 卡片"""
    category = classify_hn_category(story.title, story.url)

    # 分类颜色
    cat_colors = {
        'AI/ML': 'bg-purple-500/20 text-purple-400',
        'Startup': 'bg-muted-mint/20 text-muted-mint',
        'Tools': 'bg-electric-cyan/20 text-electric-cyan',
        'Programming': 'bg-blue-500/20 text-blue-400',
        'Science': 'bg-yellow-500/20 text-yellow-400',
        'Other': 'bg-gray-500/20 text-gray-400'
    }
    cat_class = cat_colors.get(category, cat_colors['Other'])

    # 提取域名
    domain = ''
    if story.url:
        try:
            from urllib.parse import urlparse
            domain = urlparse(story.url).netloc.replace('www.', '')
        except:
            pass

    # 热门标记
    hot_badge = ''
    if story.score > 300:
        hot_badge = '<span class="material-symbols-outlined text-glow-amber text-sm">local_fire_department</span>'

    url_to_open = story.url if story.url else story.hn_url

    # 使用中文标题（如果有），否则使用原标题
    display_title = story.title_zh if story.title_zh and lang == 'zh' else story.title
    # 如果有中文翻译，显示原标题作为副标题
    subtitle_html = ''
    if story.title_zh and lang == 'zh' and story.title_zh != story.title:
        subtitle_html = f'<p class="text-xs text-text-muted/60 mt-1 truncate">{story.title}</p>'

    return f'''
    <div class="hn-story group flex items-start gap-4 p-4 rounded-xl border border-synapse-border
                bg-synapse-card/40 hover:bg-synapse-card hover:border-glow-amber/30 transition-all cursor-pointer"
         onclick="window.open('{url_to_open}', '_blank')">
        <!-- Rank -->
        <span class="text-2xl font-bold text-text-muted font-mono w-8 shrink-0">{rank:02d}</span>

        <!-- Content -->
        <div class="flex-1 min-w-0">
            <div class="flex items-start gap-2">
                <h3 class="text-base font-medium text-white group-hover:text-glow-amber leading-snug">
                    {display_title}
                </h3>
                {hot_badge}
            </div>
            {subtitle_html}
            <div class="flex items-center flex-wrap gap-x-4 gap-y-1 mt-2 text-xs text-text-muted">
                <span class="flex items-center gap-1">
                    <span class="material-symbols-outlined text-glow-amber text-sm">arrow_upward</span>
                    {story.score} pts
                </span>
                <span class="flex items-center gap-1">
                    <span class="material-symbols-outlined text-sm">chat_bubble</span>
                    {story.comments}
                </span>
                <span>by {story.author}</span>
                {f'<span class="text-text-muted/60">{domain}</span>' if domain else ''}
                <a href="{story.hn_url}" class="text-electric-cyan hover:underline"
                   onclick="event.stopPropagation()" target="_blank">discuss</a>
            </div>
        </div>

        <!-- Category & Score -->
        <div class="flex flex-col items-end gap-2 shrink-0">
            <span class="px-2 py-0.5 rounded text-[10px] font-medium {cat_class}">{category}</span>
            <div class="px-3 py-1 rounded-lg bg-glow-amber/10 text-glow-amber text-sm font-bold">
                {story.score}
            </div>
        </div>
    </div>
    '''


def generate_hn_stories_list(stories: list[HNStory], lang: str = 'zh') -> str:
    """生成 Stories 列表"""
    items = []
    for i, story in enumerate(stories, 1):
        items.append(generate_hn_story_html(story, i, lang))

    return f'''
    <div class="space-y-3">
        {''.join(items)}
    </div>
    '''


def generate_hn_dashboard_html(stories: list[HNStory], date: str = None, lang: str = 'zh') -> str:
    """生成 HN 仪表板完整 HTML"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    date_str = date

    texts = {
        'zh': {
            'title': 'Hacker News Top Stories',
            'subtitle': '来自 Y Combinator 的实时技术脉搏',
            'search_placeholder': '搜索 Stories...',
        },
        'en': {
            'title': 'Hacker News Top Stories',
            'subtitle': 'Real-time tech pulse from Y Combinator',
            'search_placeholder': 'Search stories...',
        }
    }
    t = texts.get(lang, texts['zh'])

    stats_bar = generate_hn_stats_bar(stories, lang)
    stories_list = generate_hn_stories_list(stories, lang)
    sidebar = generate_hn_sidebar_html(lang, active_page='hn')

    return f'''<!DOCTYPE html>
<html lang="{lang}" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']} - {date_str}</title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
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

        /* Custom Scrollbar */
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
            background: #FFAB00;
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

        .nav-item-active {{
            background: rgba(255, 171, 0, 0.1);
            border-left: 3px solid #FFAB00;
            color: #fff;
        }}

        .pulse-dot {{
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .hn-story:hover {{
            transform: translateX(4px);
        }}
    </style>
</head>
<body class="h-screen w-full flex overflow-hidden font-display selection:bg-glow-amber selection:text-black">

    {sidebar}

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col h-full overflow-hidden bg-synapse-bg relative">
        <!-- Top Bar -->
        <header class="h-16 shrink-0 border-b border-synapse-border flex items-center justify-between px-6 bg-synapse-bg/80 backdrop-blur-md z-10 sticky top-0">
            <div class="flex items-center w-full max-w-md relative">
                <span class="material-symbols-outlined absolute left-3 text-text-muted">search</span>
                <input type="text" id="search-input"
                    class="w-full bg-synapse-card border border-synapse-border rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-text-muted focus:outline-none focus:border-glow-amber focus:ring-1 focus:ring-glow-amber transition-all"
                    placeholder="{t['search_placeholder']}"
                    onkeyup="filterStories(this.value)">
            </div>
            <div class="flex items-center gap-4">
                <span class="text-sm text-text-muted font-mono">{date_str}</span>
                <button onclick="window.open('https://news.ycombinator.com', '_blank')" class="p-2 text-text-muted hover:text-glow-amber transition-colors" title="Hacker News">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </div>
        </header>

        <!-- Content -->
        <div class="flex-1 overflow-y-auto p-6">
            <!-- Header -->
            <div class="mb-6">
                <div class="flex items-center gap-3 mb-2">
                    <span class="material-symbols-outlined text-glow-amber text-3xl">local_fire_department</span>
                    <h1 class="text-2xl font-bold text-white">{t['title']}</h1>
                </div>
                <p class="text-text-muted">{t['subtitle']}</p>
            </div>

            <!-- Stats -->
            {stats_bar}

            <!-- Stories List -->
            <div id="stories-container">
                {stories_list}
            </div>
        </div>
    </main>

    <script>
    function filterStories(query) {{
        const stories = document.querySelectorAll('.hn-story');
        const lowerQuery = query.toLowerCase();

        stories.forEach(story => {{
            const title = story.querySelector('h3').textContent.toLowerCase();
            if (title.includes(lowerQuery)) {{
                story.style.display = '';
            }} else {{
                story.style.display = 'none';
            }}
        }});
    }}
    </script>
</body>
</html>
'''


def save_hn_dashboard(html: str, output_dir: str = 'archives') -> str:
    """保存 HN 仪表板 HTML"""
    output_path = Path(output_dir) / 'hn.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding='utf-8')
    return str(output_path)
